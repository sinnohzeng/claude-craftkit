# 轩匠 Xuan-Jiang

**把专业方法论注入 AI —— 让 Claude Code 不只是写得快，而是写得对、改得准。**

轩匠（Xuan-Jiang）是一个 Claude Code 技能集，包含两个插件。其中 **writing-polish** 将任仲然 40 年公文写作方法论（《怎样写作》）转化为 AI 可执行的写作与审稿工作流；**workflow-toolkit** 则覆盖开发者日常工作流的全生命周期。

| Plugin | Skills | What it does |
|--------|:------:|-------------|
| [**writing-polish**](#writing-polish--写作润色审稿) | 1 (+1 pinyin alias) | 方法论驱动的写作辅助与审稿润色 |
| [**workflow-toolkit**](#workflow-toolkit--开发工作流) | 9 (+8 pinyin aliases) | Commit、文档同步、计划评审、CI 修复等 |

---

## Quick Start

**Marketplace 安装（推荐）**

```bash
# 注册 marketplace（一次性）
claude plugin marketplace add https://github.com/sinnohzeng/xuan-jiang.git

# 按需安装
claude plugin install writing-polish@xuan-jiang
claude plugin install workflow-toolkit@xuan-jiang
```

**本地 symlink（短命令）**

用 `/commit` 代替 `/workflow-toolkit:commit`，用 `/runse` 代替 `/writing-polish:writing-polish`：

```bash
git clone https://github.com/sinnohzeng/xuan-jiang.git
cd xuan-jiang && ./setup.sh
```

---

## writing-polish · 写作润色审稿

> "好文稿好文章无疑是写出来的，但更重要的是改出来的。"
> —— 任仲然《怎样写作》

### 为什么需要这个 Skill

AI 能写出流畅的文字，但缺乏**审稿的专业判断力**。它不知道什么时候该砍掉一整段「正确的废话」，不知道公文的立意要「以意役法」而非面面俱到，不知道一篇调研报告的生命线是「真实深高新活」六个字。

writing-polish 做的事情，是把《怎样写作》中沉淀的完整方法论体系——从五种思维方式、立意构思方法论、七大文体专属标准，到何其芳十二条修改要则——全部转化为 Claude 可以遵循的结构化工作流。

**不是调 prompt 让 AI「写得更好」，而是给 AI 装上一套专业编辑的审稿操作系统。**

### 两条核心工作流

```
用户请求
  │
  ├─ "帮我写 / 起草 / 搭提纲"
  │   └─ 写作辅助工作流
  │       明确任务 → 立意构思 → 搭建提纲 → 充实内容 → 语言定调
  │
  └─ "润色 / 审稿 / 帮我改"
      └─ 审稿润色工作流
          通读识别 → 结构性审查（大处着眼）→ 细节打磨（小处着手）→ 输出
```

**写作辅助**：从空白页到成稿，5 步走完。不是让 AI 自由发挥，而是按方法论约束每一步决策——选什么角度、搭什么结构、用什么材料，都有据可依。

**审稿润色**：先大后小、先减后加。先审立意主题和结构骨架，再改段落语句，最后抠字词标点。避免「一头扎进细微处，只起到校对员作用」。

### 方法论体系

writing-polish 的知识库不是一个 prompt，而是 6 份结构化参考文档，按需加载：

| 参考文档 | 内容 | 行数 |
|---------|------|:----:|
| `writing-methodology.md` | 五种思维方式 + 立意 / 构思 / 提纲 / 材料 / 语言方法论 | ~264 |
| `genre-guide.md` | 七大文体专属审查标准 | ~364 |
| `revision-checklist.md` | 何其芳十二条 + 三维系统审查 + 定稿两标准 | ~138 |
| `logic-and-structure.md` | 逻辑主线审查 + 结构模式审查 | ~119 |
| `docx-editing-guide.md` | DOCX Track Changes 编辑全指南 | ~340 |
| `gongwen-format.md` | GB/T 9704 党政公文格式规范 + python-docx 实现 | ~278 |

> **渐进加载**：skill 描述常驻上下文 → 触发时加载 SKILL.md 核心流程 → 按需读取参考文档。不浪费 token，也不丢关键知识。

### 七大文体支持

| 文体 | 核心标准 | 典型场景 |
|------|---------|---------|
| 规范性公文 | 政治性、规范性、操作性 | 通知、意见、报告、决议、纪要 |
| 领导讲话稿 | 「三个掌握」+ 实度/深度/高度/新鲜度/气势 | 会议讲话、动员部署 |
| 调研报告 | 「真实深高新活」六字标准 | 专题调研、情况报告 |
| 述职报告 | 「三个取胜」—— 以事实、数据、实绩取胜 | 年度述职、考核述职 |
| 汇报 / 发言稿 | 四种子类型各有侧重 | 汇报工作、座谈发言、对照检查 |
| 随笔杂文 | 「真情智善理美」+「有料有趣有度」 | 评论、随笔、杂感 |
| 自媒体 | 「短快真实新」+ 标题术 + 开头术 | 公众号、头条、短视频文案 |

### AI 痕迹清除

审稿时自动识别并消除 9 类 AI 行文指纹：

| AI 痕迹 | 表现 | 处理方式 |
|---------|------|---------|
| 破折号滥用 | 句中随意插入「——补充说明」 | 改为逗号衔接的完整句 |
| 括号信息倾倒 | 括号内塞大段补充 | 融入正文，超过五六字必须改写 |
| 「如果说…那么…」 | AI 最爱的比喻句式 | 改为直接判断式表述 |
| 过渡词堆砌 | 「总的来看」「值得注意的是」密集出现 | 直接陈述，去掉铺垫 |
| 冒号标题一刀切 | 所有小节标题都是「XX：YYYYYY」 | 保留最有力的，其余去掉冒号 |
| 引号过度 | 每个概念词都加引号 | 仅首次引入时加，后续不再加 |
| 引用堆砌 | 每段以「据XXX数据」开头 | 关键数据保留来源，其余移至句末 |
| 机械列举 | 大量「一是…二是…三是…」 | 部分改为自然段落叙述 |
| 逗号到底 | 超长复合句不断句 | 拆分为短句 |

### 使用方式

调用命令：`/writing-polish` 或拼音别名 `/runse`

```
# 写作辅助
帮我写一篇关于安全生产的讲话稿
搭个提纲，主题是数字化转型

# 审稿润色
帮我润色这篇文章
审稿 /path/to/speech.docx

# DOCX 修订模式
用修订模式帮我改 /path/to/document.docx

# English works too
polish this article for me
```

### 前置依赖（可选）

```bash
# DOCX 读取
brew install pandoc         # macOS
apt install pandoc          # Ubuntu/Debian

# DOCX 编辑（Track Changes 修订模式）
pip install docx-editor python-docx
```

不安装也能用——纯文本和 Markdown 无需任何依赖，DOCX 依赖仅在需要读取或回写 Word 文档时才用到。

---

## workflow-toolkit · 开发工作流

覆盖 Claude Code 编程会话的全生命周期：从计划评审到会话收尾，9 个技能 + 8 个拼音别名。

### 技能一览

| 技能 | 拼音别名 | 自动触发 | 用途 |
|------|---------|:---:|------|
| `/commit` | `/tijiao` | — | 提交 + 推送，Chinese Conventional Commits，可选 SemVer tag |
| `/sync-docs` | `/tongbu` | **Yes** | 按 DDD + SSOT 原则同步文档和记忆 |
| `/ddd` | — | — | `/sync-docs` 的快捷别名 |
| `/review-plan` | `/shenpi` | **Yes** | UX / 前端工程 / 架构三视角评审计划，最多 3 轮 |
| `/fix-ci` | `/xiufu` | — | 追踪并迭代修复 CI 流水线直到全绿 |
| `/save-plan` | `/baocun` | — | 持久化计划到 `docs/plans/YYYY-MM-DD-slug.md` |
| `/capture-lesson` | `/fupan` | **Yes** | 出错后微复盘，记录到 `docs/lessons.md` |
| `/verify-done` | `/yanzheng` | **Yes** | 跑测试 + 高级工程师视角审查，确认完成 |
| `/wrap-up` | `/shouwei` | — | 会话收尾四连：sync-docs → lesson → commit → CI |

> **拼音别名**：中文母语者可直接用拼音调用，配合 Tab 补全，输入 `/ti` + Tab 即可触发 `/tijiao`。

### 会话工作流

```
编程会话
│
├─ 工作中 ─── Claude 自动触发 /sync-docs、/capture-lesson、
│              /verify-done、/review-plan
│
├─ 随时用 ─── /commit（提交推送）
│              /fix-ci（修流水线）
│              /save-plan（存计划）
│              /ddd（快速文档同步）
│
└─ 收工时 ─── /wrap-up ──┬─ Step 1: sync-docs
                          ├─ Step 2: capture-lesson
                          ├─ Step 3: commit
                          └─ Step 4: fix-ci（可跳过）
```

---

## 跨平台安装

两个插件原生支持 Claude Code。其他 AI 编程工具可直接复制 `SKILL.md` 和 `references/` 目录：

| 工具 | 规则目录 | 格式 |
|------|---------|------|
| Claude Code | Plugin 或 `~/.claude/skills/` | Markdown |
| Claude Web | Customize → Skills（上传 ZIP） | Markdown |
| Cursor | `.cursor/rules/` | `.mdc`（Markdown + YAML frontmatter） |
| Windsurf | `.windsurf/rules/` | Markdown（12K 字符限制） |
| TRAE | `.trae/rules/` | Markdown |
| Cline | `.clinerules/` | Markdown |
| Copilot | `.github/instructions/` | Markdown + YAML |
| Augment | `.augment/rules/` | Markdown |

## 方法论来源

写作方法论全部来自 **《怎样写作》**（任仲然著，党建读物出版社，2019 年）。任仲然曾任中组部研究室主任，40 余年公文写作与审稿经验凝结为这部方法论体系。

## License

MIT. 写作方法论版权归原作者任仲然所有。

---

> "写作不是文字的简单排列组合，而是思想的创造和精神的奉献。" —— 任仲然
