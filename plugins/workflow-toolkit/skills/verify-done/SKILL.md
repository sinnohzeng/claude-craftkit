---
name: verify-done
description: >
  Use when about to claim work is complete. Runs verification, then applies
  a senior engineer review lens on top of superpowers:verification-before-completion.
argument-hint: "[检查范围，如：只检查 API 层]"
disable-model-invocation: false
---

## Task

在标记任务完成之前，证明它真的可行。本 skill 在 superpowers:verification-before-completion 的基础上增加资深工程师视角。

### Step 1: 运行验证（同 verification-before-completion）

- 运行相关测试（`pnpm test` / `pnpm lint` / `pnpm build`），贴出完整输出
- 检查 exit code，不接受"应该能过"
- 如有 API 变更，curl 验证端点

### Step 2: 资深工程师审视

以一个 P7+ 资深工程师的视角审视：
- 这个 PR 我会批准吗？哪里会被要求改？
- 有没有偷懒的地方？（硬编码、TODO、未处理的边界情况）
- 代码是否"过度工程化"或"工程化不足"？
- 是否有安全隐患？
- 是否符合项目既有 pattern 和 CLAUDE.md 规范？

### Step 3: 判定

- 如果全部通过 → 输出 Ready
- 如果有顾虑 → 列出具体问题并继续修复，不急于宣告完成

## Output

```
## Completion Check
- Tests: PASS / FAIL (output summary)
- Lint: PASS / FAIL
- Build: PASS / FAIL
- 资深工程师审视: PASS / N 个顾虑
---
结论: Ready / Not Ready (附具体顾虑)
```

$ARGUMENTS
