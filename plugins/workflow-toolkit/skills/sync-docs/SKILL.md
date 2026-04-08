---
name: sync-docs
description: >
  Use when finishing a code change that may have made documentation, memory files, or SSOT docs stale.
  Ensures code and docs stay in sync per DDD and SSOT principles.
argument-hint: "[关注的文件或模块，如：docs/spec/05-api.md]"
disable-model-invocation: false
---

## Task

按文档驱动开发（DDD）与唯一真值（SSOT）原则，同步本次改动涉及的所有文档：

### Step 1: 识别受影响文档

扫描本次改动涉及的模块，匹配可能需要同步的文档：
- `docs/spec/*.md`（架构和规范文档）
- `CLAUDE.md` / `AGENTS.md`（开发指南）
- `README.md`（项目说明）
- `docs/claude-memory/*.md`（长期记忆）
- 其他项目特定文档

### Step 2: 逐文件同步

对每个受影响文档，确保内容与代码零漂移。特别关注：
- API 端点变更 → 同步 openapi 和 spec
- 数据模型变更 → 同步 04-data-model.md
- UI 变更 → 同步 10-design-system.md
- 部署变更 → 同步运维文档

### Step 3: 经验落盘

- 成功经验和踩坑经验落盘到仓库内长期记忆（`docs/claude-memory/`）
- 确保由 git 追踪，不只存本地或全局记忆

### Rules

- 文档变更必须在同一次 commit 中，不留"文档债务"
- 如果发现文档与代码已经存在漂移，一并修复

## Output

完成后输出三项清单：
1. **同步更新的文档列表**（文件路径 + 改动摘要）
2. **新增或修改的长期记忆条目**
3. **文档债务**（如有无法当场修复的遗留问题）

$ARGUMENTS
