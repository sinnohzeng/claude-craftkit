# Evals — writing-polish v4.2 测试用例

## 目的

写作类 skill 是**主观输出**，evals 不做严格 pass/fail 评分。本目录的作用：

1. **Regression test**：每次 SKILL 改动后跑一次，确保没有退化
2. **客观可验证部分**：通过 `scripts/scan-ai-taste.sh` 验证 AI 味红线（这部分是确定性的）
3. **主观部分**：用 spawn 2 个 subagent 对比（with-skill vs baseline），人工审阅输出
4. **反向用例**：v4.2 新增"应当拒绝触发"的场景测试

## 20 条测试用例

详见 `evals.json`。覆盖：

| ID 段 | 场景类型 | 数量 |
|---|---|---|
| test-01 至 test-03 | 轻度润色 | 3 |
| test-04 至 test-06 | 中度修改 | 3 |
| test-07 至 test-09 | 深度重构 | 3 |
| test-10 至 test-12 | DOCX 修订 | 3 |
| test-13 至 test-15 | 应当拒绝触发 | 3（反向用例，v4.2 新增） |
| test-16 至 test-20 | 边界 case（极长 / 极短 / 混合格式） | 5 |

## 跑法

### A. 客观验证（自动）

```bash
# 拿到 skill 改写后的输出，跑 scan
bash scripts/scan-ai-taste.sh /path/to/revised-output.md

# 期望：exit code = 0（全部红线 = 0）
```

### B. 主观对比（半自动）

```bash
# 1. spawn baseline subagent（不加载 writing-polish skill）执行 test-01 input
# 2. spawn with-skill subagent（加载 v4.2）执行同样 input
# 3. 对比两份输出的 AI 味密度
```

### C. 回归批量跑

```bash
bash evals/test-runner.sh           # 跑全部 20 条
bash evals/test-runner.sh --baseline    # baseline 对比
bash evals/test-runner.sh --regression  # 与上次 PASS 数比较
```

可参考 Anthropic 官方 [skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) 的 evaluation loop。

## 通过标准

- **客观红线**（test-04 / test-05 / 反向用例）：scan-ai-taste.sh exit 0 = 通过
- **结构性改造**（test-01 / test-02 / test-03 / test-07 至 09）：审查报告含明确的方法论引用 + 红线检测通过
- **反向用例**：当用户说"翻译这段英文"时不应触发本 skill，应当响应"建议使用翻译工具"
- **退化判定**：with-skill 输出在 AI 味密度上**显著优于** baseline = 通过

## 维护

每次 SKILL.md 或 references/anti-ai-taste-anchors.md 重大变更后，跑全部 20 条 test，记录通过率到 `evals/regression-log.md`。

## 重要约定：规则文档与产出文档的差异

`scripts/scan-ai-taste.sh` 是**给产出文稿用的闸门**，不是给规则定义文档用的。

以下文档**不需要通过 scan**，因为它们必然 FAIL，要列举禁用词让 Claude 学习：

- `SKILL.md`：仅 §4.2 心理 grep checklist 段、§4.3 红线快速 checklist 段、frontmatter description 中列举禁用词的部分豁免（v4.2 收紧边界）
- `references/anti-ai-taste-anchors.md`：完整规则定义，整体豁免
- `references/ai-taste-examples.md`：反例对照（含原始 AI 味文本），整体豁免
- `references/failure-cases.md`：失败案例库，整体豁免
- `references/citation-spec.md`：含模糊归因反例，部分豁免
- `evals/evals.json`：测试用例输入含 AI 味样本，整体豁免

以下文档**应该通过 scan**：

- 项目根目录 `README.md`（产品介绍，面向用户）
- `TROUBLESHOOTING.md`（用户问题指引）
- `docs/research/cross-skill-benchmark.md`（对标记录）
- 任何用户提交的修改稿
- 任何写作辅助产出的初稿和定稿

dogfooding 验证范围：scan 工具是给"用户拿到的产出物"做闸门，不强求"工具自身的规则定义文档"过闸门。这是工具与规则的边界。

**v4.2 边界收紧**：SKILL.md frontmatter description 中**列举禁用词的部分**视为元论述（与 §4.2 心理 grep 同性质）豁免；其他主体表述（章节小标题、动词、引用）必须过 scan。这意味着 SKILL.md 主体里的"范文锚点""对标"等被自身规则禁的词必须改。
