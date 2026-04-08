---
name: wrap-up
description: >
  Use when a coding session is ending and you need to wrap up: sync docs,
  capture lessons, commit changes, and optionally track CI. Orchestrates
  the full session-end workflow in sequence.
argument-hint: "[commit 说明或跳过的步骤，如：skip-ci]"
disable-model-invocation: true
effort: max
---

## Overview

会话收尾一键四连。按顺序执行以下步骤，每步完成后再进入下一步。
这是一个编排层 skill，调用其他 worker skills 的工作流。

## Workflow

### Step 1: 同步文档（/sync-docs）

扫描本次改动涉及的所有文档，按 DDD + SSOT 原则同步更新。
- 识别受影响文档并逐文件同步
- 经验落盘到长期记忆
- 输出三项清单

### Step 2: 捕获经验（/capture-lesson）

回顾本次会话中是否有纠正、返工或意外：
- 如有 → 执行微复盘，记录到 docs/lessons.md 并同步 CLAUDE.md
- 如无明显纠正 → 跳过此步，输出"本次会话无需 lesson 记录"

### Step 3: 提交代码（/commit）

将所有改动提交到远端：
- 中文 Conventional Commits 格式
- Stage 相关文件（逐文件确认，不要 git add -A）
- Commit + push
- 如需打 tag 则按 SemVer 处理

### Step 4: 跟踪 CI（可选）

- 如 $ARGUMENTS 包含 "skip-ci" → 跳过此步
- 否则 → 检查 CI 状态，如有失败则迭代修复

## Rules

- 按 Step 1 → 2 → 3 → 4 严格顺序执行，不并行
- 如任一步骤失败，停下报告并等待用户决策
- Step 2 的 lesson 捕获基于本次会话上下文判断，不强制
- Step 4 默认执行，用户可通过参数跳过

## Output

每步完成后输出该步的标准格式，最终汇总：

```
## Session Wrap-Up Complete

### 文档同步
- 更新了 N 个文档：[列表]

### 经验记录
- [新增 lesson / 本次无需记录]

### 代码提交
- Commit: <hash> <message>
- Tag: <tag>（如有）
- Push: OK

### CI 状态
- [全绿 / 跳过 / N 次修复后通过]
```

$ARGUMENTS
