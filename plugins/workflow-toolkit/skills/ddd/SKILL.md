---
name: ddd
description: >
  Alias for /sync-docs. Use when finishing a code change that may have made documentation
  or memory files stale. Syncs docs, memory, and lessons per DDD and SSOT principles.
disable-model-invocation: true
---

## Task

本 skill 是 `/sync-docs` 的别名，保留 DDD（文档驱动开发）缩写作为快捷输入。

执行与 `/sync-docs` 完全相同的工作流：

1. 识别受本次改动影响的所有文档
2. 逐文件同步确保文档与代码零漂移
3. 成功经验和踩坑经验落盘到长期记忆
4. 输出三项清单（同步的文档 / 更新的记忆 / 文档债务）

$ARGUMENTS
