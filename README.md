# 张小珺商业访谈录 · 纸上纪录片

将《张小珺商业访谈录》播客的长篇深度访谈转化为适合手机/网页阅读的书籍章节。

在线阅读：**https://mally-cj.github.io/zhangxiaojun-archives/**

## 为什么做这个

纯粹为了**方便自己阅读**。播客是很棒的媒介，但信息密度太高——开车、走路、做家务的时候听，很难真正消化那些层层递进的逻辑推演和精确的商业判断。把一场访谈变成一篇可以随时翻阅、反复咀嚼的章节，是我自己最舒服的消费方式。

**这是个人项目，非商业用途。所有内容版权归《张小珺商业访谈录》及语言及世界工作室所有。**

## 致谢

- **Prompt 来源**：感谢小红书博主 **J在发光** 提供的写作 Prompt 思路
- **转录工具**：通义听悟
- **排版工具**：Claude Code
- **原始播客**：[小宇宙](https://www.xiaoyuzhoufm.com/episode/6a09d58b1b7bd502955258ab) · [Apple Podcasts](https://podcasts.apple.com/tw/podcast/141-freda%E7%9A%84%E6%8A%95%E8%B5%84%E6%9C%AD%E8%AE%B0%E7%AC%AC2%E9%9B%86-tokenmaxxing-%E6%8A%8A%E7%94%B5%E6%9C%BA%E5%A1%9E%E8%BF%9B%E8%92%B8%E6%B1%BD%E6%9C%BA-%E6%8E%A5%E5%8A%9B%E8%B5%9B%E5%8F%98%E7%AF%AE%E7%90%83%E8%B5%9B-%E5%AD%A4%E7%8B%AC-%E4%BA%BA%E7%9A%84%E8%BF%9E%E6%8E%A5/id1634356920?i=1000768308372) · [Podwise（含文字稿）](https://podwise.ai/dashboard/episodes/8012995)

## 制作流程

```
播客音频 → 通义听悟（语音转文字）→ 人工初审 → Claude Code（按 Prompt 加工）→ 人工复核 → HTML 网页
```

## 使用的 Prompt

详见 `program.md`，该文件同时也是 Claude Code 的 agent 指令文件——打开仓库说一句"看一下 program.md，开始处理"即可自动转换新内容。

## 项目结构

```
张小珺商业访谈录/
├── README.md           # 本文件（人类阅读）
├── program.md          # Agent 指令 + 写作 Prompt（AI 阅读）
├── index.html          # 目录首页
├── 原文/               # 通义听悟转录原始稿件
└── 书籍章节/           # 加工后的书籍章节（HTML）
```

## 已收录内容

| 期数 | 嘉宾 | 主题 |
|------|------|------|
| 第141期 | Freda Duan (Ultimately Capital) | Tokenmaxxing、AI组织架构、软件行业冲击、投资行业变革、焦虑与人际连接 |
