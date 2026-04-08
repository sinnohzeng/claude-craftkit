# Claude Craftkit

Personal Claude Code skill collection. Two plugins, one marketplace.

| Plugin | Skills | Description |
|--------|--------|-------------|
| **writing-polish** | 1 | Professional writing assistance based on 《怎样写作》(任仲然) |
| **workflow-toolkit** | 9 | Developer workflow skills: commit, doc sync, plan review, CI, and more |

## Quick Start

### Claude Code (Marketplace)

```bash
# Register the marketplace (once)
claude plugin marketplace add https://github.com/sinnohzeng/claude-craftkit.git

# Install plugins
claude plugin install writing-polish@claude-craftkit
claude plugin install workflow-toolkit@claude-craftkit
```

### Personal short commands (symlink)

For short `/commit` instead of `/workflow-toolkit:commit`:

```bash
git clone https://github.com/sinnohzeng/claude-craftkit.git
cd claude-craftkit
./setup.sh
```

---

## Plugin: workflow-toolkit

Developer workflow skills for daily Claude Code interactions. Covers the full session lifecycle from planning to wrap-up.

### Skills

| Skill | Usage | Auto-trigger | Description |
|-------|-------|:---:|-------------|
| `/commit` | `/commit [说明]` | No | Commit + push with Chinese Conventional Commits, optional SemVer tag |
| `/sync-docs` | `/sync-docs [范围]` | **Yes** | Sync docs and memory per DDD + SSOT principles |
| `/ddd` | `/ddd [范围]` | No | Alias for `/sync-docs` (keyboard shortcut) |
| `/review-plan` | `/review-plan [焦点]` | **Yes** | Review plan from UX, frontend, architecture perspectives. Max 3 rounds |
| `/fix-ci` | `/fix-ci [平台]` | No | Track and iteratively fix CI pipeline until green |
| `/save-plan` | `/save-plan [标题]` | No | Persist plan to `docs/plans/YYYY-MM-DD-slug.md` |
| `/capture-lesson` | `/capture-lesson [描述]` | **Yes** | Post-mortem after correction/rework, records to `docs/lessons.md` |
| `/verify-done` | `/verify-done [范围]` | **Yes** | Run tests + senior engineer review before marking done |
| `/wrap-up` | `/wrap-up [skip-ci]` | No | Session-end orchestrator: sync-docs → lesson → commit → CI |

### Session Workflow

```
Coding session
│
├── During work ── Claude auto-triggers /sync-docs, /capture-lesson,
│                  /verify-done, /review-plan when appropriate
│
├── Ad hoc ─────── /commit (push changes)
│                  /fix-ci (pipeline broke)
│                  /save-plan (persist plan)
│                  /ddd (quick doc sync)
│
└── Session end ── /wrap-up ──┬── Step 1: sync-docs
                              ├── Step 2: capture-lesson
                              ├── Step 3: commit
                              └── Step 4: fix-ci (skippable)
```

---

## Plugin: writing-polish

> **"好文稿好文章无疑是写出来的，但更重要的是改出来的。"**
> 任仲然《怎样写作》

A Claude Code skill that transforms decades of professional Chinese government writing methodology (《怎样写作》by 任仲然) into AI-executable writing assistance and revision workflows. Covers 7 genres, supports Markdown, DOCX (with Track Changes), and plain text.

### Two Core Capabilities

**Writing Assistance** — From blank page to complete draft via 5 steps: task clarification → conception → outline → content → language tuning.

**Manuscript Review** — Systematic "big-to-small" revision: theme → structure → paragraphs → words → punctuation. Uses 5 thinking modes, He Qifang's 12-point checklist, and genre-specific standards.

### Supported Genres

| Genre | Key Standards |
|-------|---------------|
| Official documents (公文) | Political correctness, standardization, operability |
| Leadership speeches (讲话稿) | "Three masteries" + five dimensions |
| Research reports (调研报告) | "真实深高新活" six-character standard |
| Work reports (述职报告) | "Three victories" — facts, data, achievements |
| Briefings and speeches (汇报/发言稿) | Four sub-types with distinct guidelines |
| Essays (随笔杂文) | "真情智善理美" + "三有五可" |
| Social media (自媒体) | "短快真实新" + headlines + opening hooks |

### AI Artifact Removal

The skill actively removes 9 types of AI writing fingerprints (em-dash overuse, parenthetical info-dumping, mechanical enumeration, etc.) to ensure output reads naturally.

### Usage

```
帮我写一篇关于安全生产的讲话稿
帮我润色这篇文章
审稿 /path/to/speech.docx
用修订模式帮我改 /path/to/document.docx
polish this article for me
```

### Skill Architecture

```
writing-polish/
├── SKILL.md                     # Core workflow (347 lines)
└── references/
    ├── writing-methodology.md   # 5 thinking modes + writing methodology
    ├── genre-guide.md           # 7 genre-specific review standards
    ├── revision-checklist.md    # He Qifang's 12-point checklist
    ├── logic-and-structure.md   # Logic + structure review
    ├── docx-editing-guide.md    # DOCX Track Changes guide
    └── gongwen-format.md        # GB/T 9704 government document format
```

Progressive loading: description always in context → SKILL.md on trigger → references on demand.

### Prerequisites (optional)

```bash
# DOCX reading
brew install pandoc    # macOS
apt install pandoc     # Ubuntu/Debian

# DOCX editing (Track Changes)
pip install docx-editor python-docx
```

---

## Cross-Platform Installation

Both plugins work natively in Claude Code. For other tools, copy the relevant `SKILL.md` and references:

| Tool | Rule Directory | Format |
|------|---------------|--------|
| Claude Web | Customize > Skills (upload ZIP) | Markdown |
| Claude Code | Plugin or `~/.claude/skills/` | Markdown |
| TRAE | `.trae/rules/` | Markdown |
| Cursor | `.cursor/rules/` | `.mdc` (Markdown + YAML) |
| Windsurf | `.windsurf/rules/` | Markdown (12K char limit) |
| Cline | `.clinerules/` | Markdown |
| Copilot | `.github/instructions/` | Markdown + YAML |
| Augment | `.augment/rules/` | Markdown |

## Methodology Source

All writing methodology is from **《怎样写作》** by 任仲然 (Party Building Books Publishing, 2019).

## License

MIT. Writing methodology copyright belongs to the original author 任仲然.

---

> "写作不是文字的简单排列组合，而是思想的创造和精神的奉献。"
