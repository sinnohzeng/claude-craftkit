#!/usr/bin/env python3
"""docx-review-workflow.py —— writing-polish v4.2 DOCX 修订一键化

把"读 docx → 转 markdown → 跑 scan → 输出 review 报告"打包为单条命令。

用法：
    python3 docx-review-workflow.py --input old.docx [--output reviewed.docx] \\
        [--mode track-changes|direct] [--author "任仲然"]

依赖：pandoc（读取）、python-docx（编辑，可选）。先跑 check-dependencies.sh 确认。

退出码：
    0  scan PASS，输出已生成
    1  scan FAIL，已输出审查报告但未生成 reviewed.docx
    2  使用错误（缺参数 / 文件不存在 / 依赖缺失）
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def check_pandoc() -> bool:
    """确认 pandoc 可用。"""
    return shutil.which("pandoc") is not None


def docx_to_markdown(docx_path: Path, md_path: Path, with_track_changes: bool = False) -> bool:
    """用 pandoc 把 docx 转为 markdown。"""
    cmd = ["pandoc", str(docx_path), "-t", "markdown", "--wrap=none"]
    if with_track_changes:
        cmd += ["--track-changes=all"]
    cmd += ["-o", str(md_path)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[FAIL] pandoc 转换失败: {result.stderr}", file=sys.stderr)
        return False
    return True


def run_scan(md_path: Path, script_dir: Path) -> tuple[int, str]:
    """跑 scan-ai-taste.sh，返回 (exit_code, output)。"""
    scan_script = script_dir / "scan-ai-taste.sh"
    result = subprocess.run(
        ["bash", str(scan_script), str(md_path)],
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout + result.stderr


def write_review_report(report_path: Path, scan_output: str, exit_code: int) -> None:
    """把 scan 输出整理成审查报告。"""
    status = "PASS" if exit_code == 0 else ("WARN" if exit_code == 2 else "FAIL")
    report = f"""# DOCX 审查报告

**状态**：{status}（scan 退出码 {exit_code}）

## scan 完整输出

```
{scan_output}
```

## 下一步

"""
    if exit_code == 0:
        report += "全部红线通过，可以交付。\n"
    elif exit_code == 2:
        report += "红线全过，软阈值有警告，建议根据 scan 警告进一步润色。\n"
    else:
        report += (
            "有红线违规，禁止交付。建议：\n"
            "1. 用 `bash scan-ai-taste.sh <file> --suggest-fix` 查具体改写建议\n"
            "2. 用 `bash auto-fix-loop.sh <file>` 自动尝试机械替换\n"
            "3. 涉及戏剧化叙事 / 大厂黑话 / 网络口语的违规需手工重构\n"
            "4. 查 `references/failure-cases.md` 看历史同类案例\n"
        )
    report_path.write_text(report)


def main() -> int:
    parser = argparse.ArgumentParser(description="DOCX 修订模式一键化")
    parser.add_argument("--input", required=True, help="输入 DOCX 路径")
    parser.add_argument("--output", help="输出 reviewed DOCX 路径（默认 <input>.reviewed.docx）")
    parser.add_argument(
        "--mode",
        choices=["track-changes", "direct"],
        default="track-changes",
        help="修订模式：track-changes 走 Word 修订模式（默认）；direct 直接修改",
    )
    parser.add_argument("--author", default="任仲然", help="修订作者名（默认 任仲然）")
    parser.add_argument(
        "--with-existing-track-changes",
        action="store_true",
        help="读取 DOCX 时保留已有的 track changes 标记",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.is_file():
        print(f"[FAIL] 输入文件不存在: {input_path}", file=sys.stderr)
        return 2

    if not check_pandoc():
        print("[FAIL] pandoc 未安装。先跑 bash scripts/check-dependencies.sh", file=sys.stderr)
        return 2

    script_dir = Path(__file__).resolve().parent
    work_dir = input_path.parent / f".{input_path.stem}-review-workdir"
    work_dir.mkdir(exist_ok=True)
    md_path = work_dir / "extracted.md"
    report_path = work_dir / "review-report.md"

    print(f"[1/3] 读取 DOCX: {input_path}")
    if not docx_to_markdown(input_path, md_path, args.with_existing_track_changes):
        return 2

    print(f"[2/3] 跑 AI 味 scan: {md_path}")
    exit_code, scan_output = run_scan(md_path, script_dir)

    print(f"[3/3] 生成审查报告: {report_path}")
    write_review_report(report_path, scan_output, exit_code)

    print()
    print("=" * 48)
    if exit_code == 0:
        print(f"[PASS] {report_path}")
        # 简化版：v4.2 第一批未实现真正的 track-changes 写回，只输出审查报告
        # 真正的修订写入需要 docx-editor，先给指引
        print("提示：v4.2 第一批仅输出审查报告。要把修改写回 DOCX，请手动用 docx-editor")
        print("      或在 Word 中按报告指引修改。完整自动写回工作流见 docx-editing-guide.md。")
        return 0
    elif exit_code == 2:
        print(f"[WARN] {report_path}")
        return 0
    else:
        print(f"[FAIL] 见 {report_path}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
