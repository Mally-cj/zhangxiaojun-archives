#!/usr/bin/env python3
"""
通用 SMTP 邮件发送脚本，可独立复制到任意项目使用。

依赖：Python >= 3.10，无需第三方包（自带 .env 解析兜底）。

用法：
    python send_email.py \
        --to user@example.com \
        --subject "测试邮件" \
        --body "这是一封测试邮件。"

配置：在当前工作目录的 .env 中填写 SMTP 变量，参见 SKILL.md。
"""

import argparse
import mimetypes
import os
import smtplib
import sys
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path
from typing import Iterable

_CWD = Path.cwd()
_ENV_PATH = _CWD / ".env"


def _load_env_file(path: Path) -> None:
    """当 python-dotenv 不可用时，用最小化解析器加载 .env。"""
    if not path.exists():
        return
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip("\"'\"")
            if key and key not in os.environ:
                os.environ[key] = value


try:
    from dotenv import load_dotenv

    load_dotenv(_ENV_PATH)
except Exception:
    _load_env_file(_ENV_PATH)


def _env(name: str, default: str | None = None) -> str | None:
    return os.getenv(name, default)


def _require_env(name: str) -> str:
    value = _env(name)
    if not value:
        raise ValueError(f"缺少环境变量: {name}，请在 .env 中配置。")
    return value


def _parse_addresses(raw: Iterable[str] | None) -> list[str]:
    if not raw:
        return []
    return [addr.strip() for item in raw for addr in item.split(",") if addr.strip()]


def _guess_mime_type(path: Path) -> tuple[str, str]:
    ctype, encoding = mimetypes.guess_type(str(path))
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"
    maintype, _, subtype = ctype.partition("/")
    return maintype or "application", subtype or "octet-stream"


def build_message(
    *,
    from_addr: str,
    from_name: str | None,
    to_addrs: list[str],
    cc_addrs: list[str],
    bcc_addrs: list[str],
    subject: str,
    body: str,
    html: bool,
    attachments: list[Path],
) -> EmailMessage:
    msg = EmailMessage()
    msg["From"] = formataddr((from_name, from_addr)) if from_name else from_addr
    msg["To"] = ", ".join(to_addrs)
    if cc_addrs:
        msg["Cc"] = ", ".join(cc_addrs)
    if bcc_addrs:
        msg["Bcc"] = ", ".join(bcc_addrs)
    msg["Subject"] = subject

    if html:
        msg.set_content(body, subtype="html", charset="utf-8")
    else:
        msg.set_content(body, charset="utf-8")

    for path in attachments:
        if not path.exists():
            raise FileNotFoundError(f"附件不存在: {path}")
        maintype, subtype = _guess_mime_type(path)
        with path.open("rb") as f:
            msg.add_attachment(
                f.read(),
                maintype=maintype,
                subtype=subtype,
                filename=path.name,
            )
    return msg


def send_message(
    msg: EmailMessage,
    *,
    smtp_host: str,
    smtp_port: int,
    smtp_user: str,
    smtp_password: str,
    use_ssl: bool,
    to_addrs: list[str],
) -> None:
    recipients = list(
        dict.fromkeys(
            to_addrs + _parse_addresses(msg["Cc"]) + _parse_addresses(msg["Bcc"])
        )
    )

    if use_ssl:
        with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=30) as server:
            server.login(smtp_user, smtp_password)
            server.send_message(msg, to_addrs=recipients)
    else:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg, to_addrs=recipients)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="通过 SMTP 发送邮件")
    parser.add_argument("--to", action="append", help="收件人邮箱，可多次指定或用逗号分隔；缺省时使用 DEFAULT_TO_EMAIL")
    parser.add_argument("--cc", action="append", help="抄送邮箱，可多次指定或用逗号分隔")
    parser.add_argument("--bcc", action="append", help="密送邮箱，可多次指定或用逗号分隔")
    parser.add_argument("--subject", required=True, help="邮件主题")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--body", help="邮件正文")
    group.add_argument("--body-file", type=Path, help="从文件读取邮件正文")
    parser.add_argument("--html", action="store_true", help="正文为 HTML")
    parser.add_argument("--attach", action="append", type=Path, help="附件路径，可多次指定")
    parser.add_argument("--dry-run", action="store_true", help="只构建邮件并打印，不发送")
    args = parser.parse_args(argv)

    to_addrs = _parse_addresses(args.to)
    cc_addrs = _parse_addresses(args.cc)
    bcc_addrs = _parse_addresses(args.bcc)

    if not to_addrs:
        default_to = _env("DEFAULT_TO_EMAIL")
        if default_to:
            to_addrs = [default_to]
        else:
            parser.error("至少需要一个收件人，或设置 DEFAULT_TO_EMAIL 环境变量")

    if args.body_file:
        body = args.body_file.read_text(encoding="utf-8")
    else:
        body = args.body or ""

    from_addr = _env("FROM_EMAIL") or _require_env("SMTP_USER")
    from_name = _env("FROM_NAME")

    msg = build_message(
        from_addr=from_addr,
        from_name=from_name,
        to_addrs=to_addrs,
        cc_addrs=cc_addrs,
        bcc_addrs=bcc_addrs,
        subject=args.subject,
        body=body,
        html=args.html,
        attachments=args.attach or [],
    )

    if args.dry_run:
        print("[DRY RUN] 邮件已构建，未发送。")
        print(f"From: {msg['From']}")
        print(f"To: {msg['To']}")
        print(f"Cc: {msg['Cc'] or '(无)'}")
        print(f"Bcc: {msg['Bcc'] or '(无)'}")
        print(f"Subject: {msg['Subject']}")
        print(f"Content-Type: {msg.get_content_type()}")
        print(f"Attachments: {[a.get_filename() for a in msg.iter_attachments()]}")
        print("--- Body ---")
        print(body)
        return 0

    send_message(
        msg,
        smtp_host=_require_env("SMTP_HOST"),
        smtp_port=int(_require_env("SMTP_PORT")),
        smtp_user=_require_env("SMTP_USER"),
        smtp_password=_require_env("SMTP_PASSWORD"),
        use_ssl=_env("SMTP_SSL", "false").lower() in ("1", "true", "yes"),
        to_addrs=to_addrs,
    )
    print(f"邮件已发送至: {', '.join(to_addrs)}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, FileNotFoundError) as exc:
        print(f"错误: {exc}", file=sys.stderr)
        sys.exit(1)
