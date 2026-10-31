"""生成 literature/文献精读台.html。

数据：literature/data/文献总表.json（130 篇，2026-10-30 生成）。
重新运行时会扫描 literature/sources/fulltext/：文件名以三位编号开头（如 045-作者-年.pdf）
的 PDF 会被识别为该编号的本地文件。
用法：python3 literature/scripts/build_reading_page.py
"""
import json
from pathlib import Path

LIT = Path(__file__).resolve().parents[1]
rows = json.loads((LIT / "data/文献总表.json").read_text(encoding="utf-8"))
ft = LIT / "sources/fulltext"
files = sorted(p.name for p in ft.glob("*.pdf")) if ft.exists() else []
supp_path = LIT / "data/fulltext-supplements-20261031.json"
supplements = json.loads(supp_path.read_text()) if supp_path.exists() else []

for r in rows:
    r["supplements"] = [s for s in supplements if s["n"] == r["n"] and (LIT / s["file"]).is_file()]
    translations = sorted((LIT / "translations").glob(f"{r['n']:03d}-*-中文译稿.html"))
    if translations:
        r["translation"] = translations[0].name
    numbered = [f for f in files if f.startswith(f"{r['n']:03d}-")]
    if numbered:
        r["file"] = numbered[0]
    elif r.get("file") and r["file"] not in files:
        r["file"] = ""

data = json.dumps(rows, ensure_ascii=False).replace("</", "<\\/")
tpl = (LIT / "scripts/reading_page_template.html").read_text(encoding="utf-8")
out = LIT / "文献精读台.html"
out.write_text(tpl.replace("__DATA__", data), encoding="utf-8")
print(f"{out}：{len(rows)} 篇，本地 PDF {sum(1 for r in rows if r.get('file'))} 篇")
