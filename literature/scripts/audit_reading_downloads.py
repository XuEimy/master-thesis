"""按当前文献总表和本机 PDF 生成下载缺口；不改变原表的阅读、证据或权限分类。"""
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[2]
LIT = ROOT / "literature"
rows = json.loads((LIT / "data/文献总表.json").read_text(encoding="utf-8"))
scope_path = LIT / "data/current-reading-scope.json"
scope = json.loads(scope_path.read_text(encoding="utf-8")) if scope_path.exists() else {}
excluded_ids = {r["n"] for r in scope.get("excluded", [])}
rows = [r for r in rows if r["n"] not in excluded_ids]
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
supp_path = LIT / "data/fulltext-supplements-20261031.json"
supp = json.loads(supp_path.read_text()) if supp_path.exists() else []
text_ids = {s["n"] for s in supp if s["kind"] == "fulltext_text" and (LIT / s["file"]).is_file()}
text_only = [r for r in missing if r["n"] in text_ids]
pending = [r for r in missing if r["n"] not in text_ids]
counts = Counter(r["acc_type"] for r in pending)
lines = [
    "# 当前文献下载缺口", "",
    f"核对日期：{today}。范围：历史总表经 `data/current-reading-scope.json` 筛选后的 {len(rows)} 篇；逐项检查本机 `literature/sources/fulltext/` 的文件及 PDF 文件头。", "",
    f"已匹配本地 PDF {len(present)} 篇，另有全文文本 {len(text_only)} 篇，待补全文 {len(pending)} 篇。目录内其他 PDF 或重复版本不计入已下载篇数；有 PDF 不代表已完成全文核读。", "",
    f"缺 PDF 的条目中，另有 {len(text_only)} 篇已保存 PMC 全文 TXT/XML（无原始图像及版式）；其余 {len(missing)-len(text_only)} 项尚未取得完整全文，书籍节选不计完整全文。逐项原因与已尝试渠道见[暂未取得全文清单](暂未取得全文-原因与渠道.md)。", "",
    "获取方式沿用 2026-10-30 总表。已补查出版社、作者和机构库公开版本；原分类不代表当前订阅权限，访问失败也不直接等于付费墙。新增文件来源及版本见 `data/fulltext-downloads-*.json`（按获取日期建账）。当前仅052、064继续列为待补全文；023已有全文文本，不再追原版PDF。书及其他移出项见[阅读与下载范围](当前阅读与下载范围.md)。", "",
    "| 原表获取方式 | 缺失篇数 |", "|---|---:|",
]
for group in ("浏览器", "浏览器·ACM", "图书馆", "图书馆（专著）"):
    lines.append(f"| {group} | {counts[group]} |")

checks_path = LIT / "data/fulltext-access-checks-20261031.json"
if checks_path.exists():
    checks = json.loads(checks_path.read_text(encoding="utf-8"))
    missing_ids = {r["n"] for r in missing}
    relevant = [c for c in checks if c["n"] in missing_ids]
    if relevant:
        lines += ["", "## 已核查的渠道限制", ""]
        for check in relevant:
            lines.append(f"- {check['n']:03d}：{check['date']}，{check['platform']}：{check['status']}。{check['boundary']}")

def table(items):
    result = ["| 编号 | 阅读级别 | 文献 | 来源 | 获取入口 |", "|---|---|---|---|---|"]
    for r in sorted(items, key=lambda x: x["n"]):
        link = f"[DOI](https://doi.org/{r['doi']})" if r.get("doi") else "按书名查询馆藏"
        cells = [f"{r['n']:03d}", ("★" if r["star"] else "") + r["tier"], f"{r['cite']}，*{r['title']}*", r.get("venue", ""), link]
        result.append("| " + " | ".join(c.replace("|", "\\|").replace("\n", " ") for c in cells) + " |")
    return result

star_missing = [r for r in missing if r["star"]]
lines += ["", "## 开题前优先文献", ""]
lines += table(star_missing) if star_missing else ["6篇★优先文献均已取得PDF。"]
for group in ("图书馆", "图书馆（专著）", "浏览器·ACM", "浏览器"):
    if counts[group]:
        lines += ["", f"## {group}（{counts[group]} 篇）", ""] + table([r for r in pending if r["acc_type"] == group])
lines += ["", "下载后按三位编号命名，例如 `056-作者-年份.pdf`，存入 `literature/sources/fulltext/`。运行以下命令更新缺口与精读页面：", "", "```sh", "python3 literature/scripts/audit_reading_downloads.py", "python3 literature/scripts/build_reading_page.py", "```", ""]
out = LIT / "当前文献下载缺口.md"
out.write_text("\n".join(lines), encoding="utf-8")
print(f"{out}：PDF {len(present)}，文本 {len(text_only)}，待补全文 {len(pending)}；{dict(counts)}")
