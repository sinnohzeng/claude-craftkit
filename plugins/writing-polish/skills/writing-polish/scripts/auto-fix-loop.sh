#!/usr/bin/env bash
# auto-fix-loop.sh —— writing-polish v4.2 自动修复循环
#
# scan 失败时调用此脚本，对常见违规做机械替换尝试 1 至 2 轮。
# 多轮失败后退出，交人工处理。
#
# 注意：本脚本只做"高置信度机械替换"（如破折号 → 逗号、ASCII 直引号 → 弯引号）。
# 涉及语义的违规（如戏剧化叙事、大厂黑话）不机械替换，因为 anchors §1.5 明确要求重构整段表述。
#
# 用法：
#   bash auto-fix-loop.sh /path/to/file.md
#   bash auto-fix-loop.sh /path/to/file.md --max-rounds 3
#
# 退出码：
#   0  最终通过 scan
#   1  多轮修复后仍失败
#   2  使用错误

set -uo pipefail

FILE="${1:-}"
MAX_ROUNDS=2
shift 2>/dev/null || true
while [ $# -gt 0 ]; do
    case "$1" in
        --max-rounds) MAX_ROUNDS="$2"; shift 2 ;;
        *) shift ;;
    esac
done

if [ -z "$FILE" ] || [ ! -f "$FILE" ]; then
    echo "用法: bash auto-fix-loop.sh <file.md> [--max-rounds N]"
    exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [ -t 1 ]; then
    RED='\033[0;31m'; YEL='\033[0;33m'; GRN='\033[0;32m'; NC='\033[0m'
else
    RED=''; YEL=''; GRN=''; NC=''
fi

apply_safe_fixes() {
    local f="$1"
    local tmp
    tmp=$(mktemp)
    # 安全机械替换（高置信度）
    python3 << PYEOF
import re, sys
text = open("$f").read()

# 破折号 → 逗号或句号（破折号前后是中文时改逗号）
text = re.sub(r'([一-鿿])——([一-鿿])', r'\1，\2', text)
text = re.sub(r'([一-鿿])—([一-鿿])', r'\1，\2', text)

# ASCII 直引号 → 弯引号（中文上下文）
def replace_ascii_quotes(line):
    cn_pattern = '[一-鿿]'
    # 保护 markdown code block 内
    if line.strip().startswith('\`\`\`'):
        return line
    # 双引号配对替换：相邻两个 " 中第一个变 "，第二个变 "
    out = []
    in_dq = False
    for ch in line:
        if ch == '"':
            out.append('”' if in_dq else '“')
            in_dq = not in_dq
        elif ch == "'":
            out.append("’" if in_dq else "‘")
        else:
            out.append(ch)
    return ''.join(out)

# 仅当行包含中文时做引号替换
new_lines = []
for line in text.split('\n'):
    if re.search(r'[一-鿿]', line):
        new_lines.append(replace_ascii_quotes(line))
    else:
        new_lines.append(line)
text = '\n'.join(new_lines)

# 直角引号 → 弯引号
text = text.replace('「', '“').replace('」', '”')
text = text.replace('『', '“').replace('』', '”')

# 中文段落内英文标点 → 中文标点（限"中文-英文标点-中文"模式）
text = re.sub(r'([一-鿿]),(\s*[一-鿿])', r'\1，\2', text)
text = re.sub(r'([一-鿿]):(\s*[一-鿿])', r'\1：\2', text)
text = re.sub(r'([一-鿿]);(\s*[一-鿿])', r'\1；\2', text)
# 句尾英文句号（中文前不加点，因为句尾常带换行）
text = re.sub(r'([一-鿿])\.(\s*\n)', r'\1。\2', text)

open("$tmp", "w").write(text)
PYEOF
    mv "$tmp" "$f"
}

ROUND=0
echo "================================================"
echo "  auto-fix-loop v4.2"
echo "  目标文件: $FILE"
echo "  最大轮数: $MAX_ROUNDS"
echo "================================================"

# 备份
BACKUP="${FILE}.before-autofix"
cp "$FILE" "$BACKUP"
echo "已备份原始文件至: $BACKUP"
echo

# 第 0 轮：先跑一次 scan 看初始状态
echo "▼ 初始 scan..."
if bash "$SCRIPT_DIR/scan-ai-taste.sh" "$FILE" >/dev/null 2>&1; then
    printf "${GRN}✅ 初始已 PASS，无需修复${NC}\n"
    rm "$BACKUP"
    exit 0
fi

# 修复循环
while [ "$ROUND" -lt "$MAX_ROUNDS" ]; do
    ROUND=$((ROUND + 1))
    echo
    echo "▼ 第 $ROUND 轮自动修复..."
    apply_safe_fixes "$FILE"
    echo "  应用安全机械替换：破折号、ASCII 直引号、直角引号、中文段落英文标点"
    echo
    echo "  重新 scan..."
    if bash "$SCRIPT_DIR/scan-ai-taste.sh" "$FILE" >/dev/null 2>&1; then
        printf "${GRN}✅ 第 %d 轮后 PASS${NC}\n" "$ROUND"
        echo "原始备份: $BACKUP"
        echo "如需还原: mv $BACKUP $FILE"
        exit 0
    fi
done

echo
printf "${YEL}⚠ %d 轮后仍未通过${NC}\n" "$MAX_ROUNDS"
echo "下一步建议："
echo "  1. 运行 bash scan-ai-taste.sh \"$FILE\" --suggest-fix 看具体改写建议"
echo "  2. 涉及戏剧化叙事 / 大厂黑话 / 网络口语的违规需手工重构（机械替换不通过）"
echo "  3. 查 references/failure-cases.md 看历史同类案例"
echo "原始备份: $BACKUP"
exit 1
