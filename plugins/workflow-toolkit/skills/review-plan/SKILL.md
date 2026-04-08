---
name: review-plan
description: >
  Use when an implementation plan has been created or updated and needs quality review
  before execution. Reviews from UX, frontend engineering, and architecture perspectives.
argument-hint: "[评审焦点，如：性能、可维护性、安全性]"
disable-model-invocation: false
effort: max
---

## Task

对当前工作计划做严格评审，从三个视角逐一扫描：

### 视角 1: 用户体验（UX）

- 交互流程是否自然、符合用户心智模型？
- 加载状态、错误状态、空状态是否覆盖？
- 可访问性（a11y）是否考虑？
- 移动端适配是否到位？

### 视角 2: 前端工程化

- 组件划分是否合理？是否复用了现有组件？
- 状态管理是否清晰？是否有不必要的全局状态？
- 性能瓶颈是否预判（大列表、频繁 re-render、bundle size）？
- 是否遵循项目既有 pattern（参考 CLAUDE.md 和 AGENTS.md）？

### 视角 3: 软件架构

- 数据流是否清晰？前后端边界是否合理？
- 是否引入了不必要的复杂度？能否更简单？
- 安全性是否考虑（XSS、CSRF、注入、权限）？
- 可测试性如何？

### Rules

- 所有发现的问题直接迭代回计划本身——不分优先级、不留 TODO、不推迟
- 评审结束输出「本轮新增改动清单」
- **退出条件**：连续一轮无重大问题即标记完成；最多迭代三轮

## Output

每轮输出：

```
## Round N/3
### UX 发现
...
### 前端工程发现
...
### 架构发现
...
---
结论: 通过 / 继续迭代
```

$ARGUMENTS
