---
name: capture-lesson
description: >
  Use when a correction, rework, or unexpected issue just occurred and the lesson
  should be captured immediately. Records what went wrong, root cause, and prevention.
argument-hint: "[发生了什么，如：API 字段命名错误导致返工]"
disable-model-invocation: false
---

## Task

刚刚发生了纠正、返工或意外。立刻做一次微复盘。

### Workflow

1. **记录 Lesson**：用简洁结构写清：
   - **做错了什么**：一句话描述
   - **根因**：为什么会发生
   - **预防措施**：下次如何避免
2. **追加到 `docs/lessons.md`**：
   - 如文件不存在则创建，包含标题和日期索引
   - 格式：`### YYYY-MM-DD: <标题>`，下方三点（做错/根因/预防）
3. **判断同步去向**：
   - 如果是通用规则（跨项目适用）→ 同步到 `CLAUDE.md`
   - 如果是项目特定经验 → 同步到 `docs/claude-memory/feedback_*.md`
   - 如果只是一次性事件 → 仅记录 lessons.md，不同步

## Output

```
## Lesson Captured
- 条目: <标题>
- 文件: docs/lessons.md
- 同步: CLAUDE.md / feedback_xxx.md / 仅 lessons.md
```

$ARGUMENTS
