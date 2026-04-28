# 常见问题指引（writing-polish v4.2）

> 本文件按“症状 / 原因 / 解决”三段组织。先跑 `bash plugins/writing-polish/skills/writing-polish/scripts/check-dependencies.sh` 排查依赖。
>
> 本文件为元论述（讲解规则使用），列举大量违规词作教学示例，scan-ai-taste.sh 会跳过整文扫描。

<!-- scan-skip -->

## 1. scan 一直 FAIL，怎么办？

### 症状

跑 `bash scripts/scan-ai-taste.sh draft.md` 反复 FAIL。

### 原因

按出现频率排序：

1. 戏剧化叙事词（三层防御 / 闸门 / 翻车 / 跑通）机械替换不通过
2. 大厂黑话（抓手 / 闭环 / 对标 / 复盘）已成思维定式
3. 客服段尾（希望对您有帮助 / 有问题继续提问）漏删
4. 标点（破折号 / ASCII 直引号 / 直角引号）忘换
5. 元注释（作为一个 AI 助手 / 以下是几点说明）开头未清

### 解决

**第一步**：跑带建议的 scan：

```bash
bash plugins/writing-polish/skills/writing-polish/scripts/scan-ai-taste.sh draft.md --suggest-fix
```

每条违规会附改写建议。

**第二步**：标点 / 直引号类机械违规可用自动修复：

```bash
bash plugins/writing-polish/skills/writing-polish/scripts/auto-fix-loop.sh draft.md
```

会备份原文为 `draft.md.before-autofix`，最多 2 轮尝试。

**第三步**：戏剧化与大厂黑话不能机械替换。查 `references/failure-cases.md` 看历史同类 case 的重写过程。核心是把表达拉回事实陈述。

## 2. DOCX 打不开 / 转换失败

### 症状

DOCX 文件交给 SKILL 时报"pandoc 转换失败"或"找不到 pandoc 命令"。

### 原因

依赖未装。

### 解决

```bash
bash plugins/writing-polish/skills/writing-polish/scripts/check-dependencies.sh
```

按提示装：

- macOS：`brew install pandoc`
- Ubuntu / Debian：`apt install pandoc`
- 修订模式还需：`pip install python-docx docx-editor`

## 3. 不知道自己属于哪个文体

### 症状

写稿时不确定走"公文 / 讲话稿 / 调研报告 / 述职报告 / 汇报发言稿 / 随笔杂文 / 自媒体"哪条工作流。

### 解决

按下面的判断：

| 用户身份 | 主要功能 | 文体 |
|---|---|---|
| 党政机关单位 | 印发命令 / 通知 / 决议 | 规范性公文 |
| 党政领导个人 | 大会讲话 / 会议讲话 | 领导讲话稿 |
| 调研课题组 | 现状诊断 / 政策建议 | 调研报告 |
| 个人 / 单位领导 | 年度述职 / 考核述职 | 述职报告 |
| 单位向上汇报 | 工作汇报 / 座谈交流 | 汇报发言稿 |
| 个人发表观点 | 评论 / 杂感 / 散文 | 随笔杂文 |
| 公众号 / 头条 / 短视频 | 公开传播 | 自媒体 |

不确定时按"主要场合 + 主要受众"二维定位。详细标准见 `plugins/writing-polish/skills/writing-polish/references/genre-guide.md`。

## 4. 修订模式（Track Changes）每段都改了，看着乱

### 症状

DOCX 跑修订模式后整篇全是红色修改痕迹，难以审阅。

### 原因

修订模式 / 大范围重写 / 简要版新写三种场景未正确区分。修订模式应当"定点精修"。

### 解决

明确告知 SKILL：

- 客户已给批注版要求 track changes → "用修订模式定点精修"
- 想要重新组织全文 → "重写这份文档" → 不开 track changes
- 想压缩到简要版 → "起草一份 5 页简要版" → 不开 track changes

详细判定优先级见 `SKILL.md` §3.3。

## 5. 写作辅助生成的文稿空洞，全是套话

### 症状

让 SKILL 起草，输出全是"在新时代背景下""全方位推进""高质量发展"。

### 原因

用户 prompt 没给具体内容素材，AI 缺米下锅，反射性堆套话。

### 解决

**给具体素材**。比如不说"帮我起草关于数字化转型的讲话"，改说：

> 帮我起草一份关于数字化转型的市级会议讲话稿，长度 8 至 10 分钟。背景：我市过去三年在 X 领域试点的成果是 A、B、C 三件事，准备在大会上分享给 18 个区县。受众主要是各区县分管领导。要重点讲三件事：试点成效、推广路径、配套政策。

材料越具体，输出越实在。

## 6. scan 报"句长标准差 < 8"

### 症状

跑 scan 时其他都过，唯独"句长方差"红色警告。

### 原因

句长过于均匀（每句 18 至 22 字），是 AI 输出指纹。人写的中文有长短交错。

### 解决

**改写策略**：

- 找几个长句拆成两短句
- 找几个短句合并扩展
- 加一两句一个字到三个字的极短句（如"这是问题。""不行。""得改。"）做节奏

人类写作的节奏是长短交错，目标标准差 ≥ 8，平均 25 至 35 字。

## 7. 中文里出现 ASCII 直引号怎么办

### 症状

scan 报"§1.4.111 ASCII 直引号"违规。

### 原因

macOS / iOS 默认 smart quotes 开启时会自动转弯引号；但若关闭、或来自代码 / 终端复制粘贴，就是 ASCII 直引号。

### 解决

```bash
bash plugins/writing-polish/skills/writing-polish/scripts/auto-fix-loop.sh draft.md
```

会自动批量替换为大陆国标弯引号 `""` `''`。也可手动：

- macOS：开"系统偏好 → 键盘 → 文本"勾选"使用智能引号"
- VS Code：装"Smart Quotes"扩展
- Word：默认开启"自动套用格式 → 智能引号"

## 8. 反向用例：我想翻译 / 写代码 / 分析数据

### 症状

让 SKILL 翻译英文、review 代码、分析 Excel 数据。

### 原因

本 SKILL 不处理这三类场景，详见 SKILL.md frontmatter。

### 解决

直接说明用途：

- 翻译 → 用通用翻译工具或专门的翻译 skill
- 代码 review → 用代码 review 工具或 `code-review` skill
- 数据分析 → 用 pandas / Excel 或专门的数据 skill

## 9. SKILL.md 自身跑 scan 也 FAIL 了

### 症状

`bash scripts/scan-ai-taste.sh plugins/writing-polish/skills/writing-polish/SKILL.md` 报 FAIL。

### 原因

预期行为。SKILL.md 含元论述段（§4.2 心理 grep checklist 列举禁用词）。

### 解决

参见 `evals/README.md`"重要约定：规则文档与产出文档的差异"。SKILL.md 整体不强求过 scan，仅"主体非元论述段"应当过。v4.2 已收紧豁免边界，但 §4.2 / §4.3 列举段必然 FAIL。

## 10. 想看 SKILL 历史变更

### 解决

- 项目根 README.md 末尾"方法论与规范来源"段含完整版本表
- 详细 changelog 见 `docs/research/cross-skill-benchmark.md`
- 历史失败案例见 `references/failure-cases.md`

<!-- /scan-skip -->
