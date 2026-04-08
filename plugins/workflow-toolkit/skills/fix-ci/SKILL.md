---
name: fix-ci
description: >
  Use when a CI pipeline has failed or when you need to monitor pipeline status
  and iteratively fix issues until all pipelines are green.
argument-hint: "[CI 平台或流水线名，如：CodeArts、GitHub Actions]"
disable-model-invocation: true
allowed-tools: Bash(git *), Bash(gh *), Bash(curl *), Bash(ssh *)
---

## Context

- Current branch: !`git branch --show-current`
- Latest commit: !`git log --oneline -3`

## Task

持续跟踪 CI 流水线状态，迭代修复直到全绿。

### Workflow

1. **获取状态**：通过 gh / curl / ssh 获取流水线状态和日志
2. **定位失败**：逐行阅读错误日志，定位根因
3. **修复**：实施修复并提交
4. **验证**：等待新一轮 CI，重复直到全绿

### Rules

- 中途无需停下等用户确认，除非遇到需要业务决策的歧义点
- 每次修复后简要记录失败原因与修复手段
- 不要用 `--no-verify` 跳过 hook
- 不要注释掉失败的测试来"修复"CI

## Output

每轮修复输出：
| 轮次 | 失败原因 | 修复手段 | 结果 |
|------|---------|---------|------|
| 1    | ...     | ...     | PASS/FAIL |

最终状态：全绿 / 仍有失败（附原因）

$ARGUMENTS
