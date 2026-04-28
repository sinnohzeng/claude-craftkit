#!/usr/bin/env bash
# check-dependencies.sh —— writing-polish v4.2 依赖检查
#
# 触发 SKILL 前可选预检：pandoc / Python / docx-editor 是否齐备。
# 缺什么给什么命令，不让用户卡在"为什么 pandoc 找不到"上。
#
# 用法：bash check-dependencies.sh
# 退出码：
#   0  全部齐备
#   1  有缺失依赖（基础功能受限）
#   2  有缺失依赖（DOCX 功能受限）

set -uo pipefail

if [ -t 1 ]; then
    RED='\033[0;31m'; YEL='\033[0;33m'; GRN='\033[0;32m'; NC='\033[0m'
else
    RED=''; YEL=''; GRN=''; NC=''
fi

MISSING_CORE=0
MISSING_DOCX=0

echo "================================================"
echo "  writing-polish v4.2 依赖检查"
echo "================================================"
echo

# ---- 核心依赖 ----
echo "▼ 核心依赖（Markdown / 纯文本场景必需）"

if command -v python3 >/dev/null 2>&1; then
    PYV=$(python3 --version 2>&1 | awk '{print $2}')
    PYMAJOR=$(echo "$PYV" | cut -d. -f1)
    PYMINOR=$(echo "$PYV" | cut -d. -f2)
    if [ "$PYMAJOR" -ge 3 ] && [ "$PYMINOR" -ge 7 ]; then
        printf "  ${GRN}✓ python3 %s${NC}\n" "$PYV"
    else
        printf "  ${YEL}⚠ python3 %s（需 3.7+）${NC}\n" "$PYV"
        MISSING_CORE=$((MISSING_CORE + 1))
    fi
else
    printf "  ${RED}✗ python3 未安装${NC}\n"
    echo "    macOS: brew install python3"
    echo "    Ubuntu: apt install python3"
    MISSING_CORE=$((MISSING_CORE + 1))
fi

if command -v bash >/dev/null 2>&1; then
    BASHV=$(bash --version | head -1 | awk '{print $4}')
    printf "  ${GRN}✓ bash %s${NC}\n" "$BASHV"
else
    printf "  ${RED}✗ bash 未安装（不应发生）${NC}\n"
    MISSING_CORE=$((MISSING_CORE + 1))
fi

if command -v grep >/dev/null 2>&1; then
    printf "  ${GRN}✓ grep${NC}\n"
else
    printf "  ${RED}✗ grep 未安装（不应发生）${NC}\n"
    MISSING_CORE=$((MISSING_CORE + 1))
fi

echo

# ---- DOCX 依赖 ----
echo "▼ DOCX 依赖（Word 文档读写场景必需）"

if command -v pandoc >/dev/null 2>&1; then
    PANV=$(pandoc --version 2>&1 | head -1 | awk '{print $2}')
    printf "  ${GRN}✓ pandoc %s${NC}\n" "$PANV"
else
    printf "  ${YEL}⚠ pandoc 未安装（DOCX 读取受限）${NC}\n"
    echo "    macOS: brew install pandoc"
    echo "    Ubuntu: apt install pandoc"
    echo "    Debian: apt install pandoc"
    echo "    docs: https://pandoc.org/installing.html"
    MISSING_DOCX=$((MISSING_DOCX + 1))
fi

if python3 -c "import docx" 2>/dev/null; then
    printf "  ${GRN}✓ python-docx${NC}\n"
else
    printf "  ${YEL}⚠ python-docx 未安装（DOCX 编辑受限）${NC}\n"
    echo "    pip install python-docx"
    MISSING_DOCX=$((MISSING_DOCX + 1))
fi

if python3 -c "import docx_editor" 2>/dev/null; then
    printf "  ${GRN}✓ docx-editor${NC}\n"
else
    printf "  ${YEL}⚠ docx-editor 未安装（修订模式受限）${NC}\n"
    echo "    pip install docx-editor"
    MISSING_DOCX=$((MISSING_DOCX + 1))
fi

echo

# ---- 总结 ----
echo "================================================"
if [ "$MISSING_CORE" -eq 0 ] && [ "$MISSING_DOCX" -eq 0 ]; then
    printf "${GRN}✅ 全部依赖齐备${NC}\n"
    exit 0
elif [ "$MISSING_CORE" -gt 0 ]; then
    printf "${RED}✗ 核心依赖缺失 %d 项，基础 scan 功能受限${NC}\n" "$MISSING_CORE"
    exit 1
else
    printf "${YEL}⚠ DOCX 依赖缺失 %d 项，Markdown 功能正常${NC}\n" "$MISSING_DOCX"
    echo "如不处理 Word 文档可忽略此警告"
    exit 2
fi
