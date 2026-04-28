#!/usr/bin/env python3
"""中文标点与中英混排检测器（红线 §1.4.111 / §1.4.112 / §1.4.113）

用法：python3 check-cn-quotes.py <file.md>
退出码：0=PASS，1=FAIL（任意一项违规）

检测：
1. ASCII 直引号 " ' 在中文上下文（应当用大陆国标弯引号 " " ' '）
2. 直角引号「」『』在中文里（港台 / 日式标点，大陆党政公文不用）
3. 加号 + 和等号 = 在中文上下文做并列或定义连词（数学符号代替自然语言）
4. 半中半英术语（中文字符紧邻英文单词，非保留专名）

跳过：
- fenced code blocks (```...```)
- inline code (`...`)
- URL 链接（http / https / www）
"""
import re
import sys

# 保留专名清单：技术术语、产品名、公司名等首次出现可与中文紧邻
RESERVED_TERMS = {
    'GitHub', 'GB', 'GBT', 'DOCX', 'Markdown', 'YAML', 'JSON', 'API',
    'SKILL', 'README', 'LICENSE', 'CONTRIBUTING', 'SECURITY',
    'Anthropic', 'Claude', 'ChatGPT', 'Wikipedia', 'OpenAI',
    'Firecrawl', 'GPTZero',
    'pandoc', 'python', 'docx', 'editor', 'pip', 'pre',
    'L1', 'L2', 'L3', 'PASS', 'FAIL', 'WARN',
    'PDF', 'CSV', 'XML', 'HTML', 'CSS',
    'macOS', 'Linux', 'Windows', 'Ubuntu', 'Debian',
    'AI', 'RLHF', 'TOC', 'CI', 'OOXML',
    'MIT', 'GPL', 'URL', 'TTL', 'CDN',
    'OpenAI', 'Cursor', 'Windsurf', 'Cline', 'Copilot',
}


def strip_code_and_links(text: str) -> str:
    """移除 code block / inline code / URL，保留行号。"""
    text = re.sub(r'```.*?```', lambda m: '\n' * m.group().count('\n'), text, flags=re.DOTALL)
    text = re.sub(r'`[^`]*`', '', text)
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'www\.\S+', '', text)
    return text


def check_ascii_quotes(text: str) -> list[tuple[int, str]]:
    """规则 1：ASCII 直引号 / ' 在中文上下文。"""
    cn = r'[一-鿿]'
    pat = re.compile(rf'{cn}["\']|["\']{cn}')
    return [
        (i, line[:120])
        for i, line in enumerate(text.split('\n'), 1)
        if pat.search(line)
    ]


def check_corner_quotes(text: str) -> list[tuple[int, str]]:
    """规则 2：直角引号「」『』（港台 / 日式，大陆禁用）。"""
    pat = re.compile(r'[「」『』]')
    return [
        (i, line[:120])
        for i, line in enumerate(text.split('\n'), 1)
        if pat.search(line)
    ]


def check_math_symbols(text: str) -> list[tuple[int, str]]:
    """规则 3：加号 + 等号 = 在中文上下文做并列连词或定义。"""
    cn = r'[一-鿿]'
    # + 周围有中文（中英混排数学表达式不算）
    plus_pat = re.compile(rf'{cn}\s*\+\s*{cn}')
    # = 周围有中文（"X = Y" 表示等同）
    eq_pat = re.compile(rf'{cn}\s*=\s*{cn}')
    # → 中文上下文（流程箭头）
    arrow_pat = re.compile(rf'{cn}\s*[→⇒]\s*{cn}')
    out = []
    for i, line in enumerate(text.split('\n'), 1):
        if plus_pat.search(line) or eq_pat.search(line) or arrow_pat.search(line):
            out.append((i, line[:120]))
    return out


def check_mixed_terms_strict(text: str) -> list[tuple[int, str]]:
    """规则 4 严格：中文紧贴英文（无空格），是中英缝合词。"""
    cn = r'[一-鿿]'
    # 中文-紧贴-英文 或 英文-紧贴-中文（无空格分隔）
    pat = re.compile(rf'{cn}[A-Za-z]+|[A-Za-z]+{cn}')
    reserved_lower = {t.lower() for t in RESERVED_TERMS}
    out = []
    for i, line in enumerate(text.split('\n'), 1):
        for m in pat.finditer(line):
            word_match = re.search(r'[A-Za-z]+', m.group())
            if not word_match:
                continue
            word = word_match.group()
            if word.lower() in reserved_lower:
                continue
            if re.match(r'^v?\d+(\.\d+)*$', word):
                continue
            if len(word) == 1:
                continue
            out.append((i, line[:120]))
            break
    return out


def main(path: str) -> int:
    raw = open(path).read()
    text = strip_code_and_links(raw)

    rules = [
        ('§1.4.111 ASCII 直引号（中文上下文）', check_ascii_quotes(text)),
        ('§1.4.111 直角引号 「」『』（港台 / 日式）', check_corner_quotes(text)),
        ('§1.4.112 数学符号代替自然语言（+ = →）', check_math_symbols(text)),
        ('§1.4.113 中英紧贴缝合词（无空格）', check_mixed_terms_strict(text)),
    ]

    total = sum(len(v) for _, v in rules)
    for name, violations in rules:
        print(f'RULE={name}|COUNT={len(violations)}')
        for line_no, content in violations[:5]:
            print(f'  {line_no}:{content}')

    print(f'TOTAL={total}')
    return 1 if total else 0


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('用法: python3 check-cn-quotes.py <file.md>', file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
