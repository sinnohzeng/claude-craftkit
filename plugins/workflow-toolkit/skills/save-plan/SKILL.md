---
name: save-plan
description: >
  Use when the current session has produced a work plan that should be persisted
  to the project's docs/plans/ directory for version control and future reference.
argument-hint: "[计划标题，如：用户认证重构]"
disable-model-invocation: true
---

## Task

将当前工作计划持久化保存到项目文档中。

### Workflow

1. **确定保存路径**：`docs/plans/YYYY-MM-DD-<slug>.md`
   - slug 从 $ARGUMENTS 或计划标题生成（小写、连字符分隔）
   - 如 `docs/plans/` 目录不存在则创建
2. **写入计划文件**：保留计划的完整内容（Context、设计、步骤、验证方案）
3. **提示后续**：保存完成后，提示用户可运行 `/sync-docs` 同步相关文档

### Rules

- 本 skill 只负责保存计划文件，不负责同步文档和记忆（那是 `/sync-docs` 的职责）
- 文件名必须包含日期以便追溯

## Output

```
## Plan Saved
- Path: docs/plans/YYYY-MM-DD-slug.md
- Size: N lines
- 提示: 如需同步文档和记忆，请运行 /sync-docs
```

$ARGUMENTS
