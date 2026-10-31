"""按当前文献总表和本机 PDF 生成下载缺口；不改变原表的阅读、证据或权限分类。"""
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[2]
LIT = ROOT / "literature"
rows = json.loads((LIT / "data/文献总表.json").read_text(encoding="utf-8"))
pdfs = sorted((LIT / "sources/fulltext").glob("*.pdf"))
present, missing = [], []
for row in rows:
    numbered = [p for p in pdfs if p.name.startswith(f"{row['n']:03d}-")]
    named = LIT / "sources/fulltext" / row.get("file", "")
    candidates = numbered or ([named] if named.is_file() else [])
    if candidates and candidates[0].read_bytes().startswith(b"%PDF-"):
        present.append(row)
    else:
        missing.append(row)

today = datetime.now(ZoneInfo("Asia/Shanghai")).date().isoformat()
counts = Counter(r["acc_type"] for r in missing)
lines = [
    "# 当前文献下载缺口", "",
    f"核对日期：{today}。范围：`literature/data/文献总表.json` 的 {len(rows)} 篇；逐项检查本机 `literature/sources/fulltext/` 的文件及 PDF 文件头。", "",
    f"已匹配本地 PDF {len(present)} 篇，缺失 {len(missing)} 篇。目录内其他 PDF 或重复版本不计入已下载篇数；有 PDF 不代表已完成全文核读。", "",
    "获取方式沿用 2026-10-30 总表。2026-10-31 已补查出版社、作者和机构库公开版本；原分类不代表当前订阅权限，访问失败也不直接等于付费墙。新增文件来源及版本见 `data/fulltext-downloads-20261031.json`。当前剩余条目仍需继续获取，部分受登录、验证或网络限制。", "",
    "| 原表获取方式 | 缺失篇数 |", "|---|---:|",
]
for group in ("浏览器", "浏览器·ACM", "图书馆", "图书馆（专著）"):
    lines.append(f"| {group} | {counts[group]} |")

def table(items):
    result = ["| 编号 | 阅读级别 | 文献 | 来源 | 获取入口 |", "|---|---|---|---|---|"]
    for r in sorted(items, key=lambda x: x["n"]):
        link = f"[DOI](https://doi.org/{r['doi']})" if r.get("doi") else "按书名查询馆藏"
        cells = [f"{r['n']:03d}", ("★" if r["star"] else "") + r["tier"], f"{r['cite']}，*{r['title']}*", r.get("venue", ""), link]
        result.append("| " + " | ".join(c.replace("|", "\\|").replace("\n", " ") for c in cells) + " |")
    return result

lines += ["", "## 开题前优先文献中缺失的全文", ""] + table([r for r in missing if r["star"]])
for group in ("图书馆", "图书馆（专著）", "浏览器·ACM", "浏览器"):
    lines += ["", f"## {group}（{counts[group]} 篇）", ""] + table([r for r in missing if r["acc_type"] == group])
lines += ["", "下载后按三位编号命名，例如 `056-作者-年份.pdf`，存入 `literature/sources/fulltext/`。运行以下命令更新缺口与精读页面：", "", "```sh", "python3 literature/scripts/audit_reading_downloads.py", "python3 literature/scripts/build_reading_page.py", "```", ""]
out = LIT / "当前文献下载缺口.md"
out.write_text("\n".join(lines), encoding="utf-8")
print(f"{out}：已有 {len(present)}，缺失 {len(missing)}；{dict(counts)}")
