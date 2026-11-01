from pathlib import Path
import fitz,json,re,html
ROOT=Path(__file__).resolve().parents[3];D=Path(__file__).parent
src=fitz.open(next((ROOT/'literature/sources/fulltext').glob('029-*.pdf')))
d=fitz.open(ROOT/'output/pdf/029-线索类型与自传体记忆-中文待验收.pdf')
# Restore DOI removed by overlapping original date font metrics.
r=d[0].insert_htmlbox(fitz.Rect(39,641,507,653.3),'https://doi.org/10.1016/j.concog.2025.103983',css='body{font-size:7pt;margin:0;color:#006699}',scale_low=1)
assert r[0]>=0
# Translate platform navigation labels while retaining the journal name and branding.
for rect in [[202,56,350,72],[176,114,375,125]]:d[0].add_redact_annot(fitz.Rect(rect),fill=False)
d[0].apply_redactions(images=0,graphics=0)
for rect,t in [([202,56,350,72],'目录见 ScienceDirect'),([176,114,390,127],'期刊主页：www.elsevier.com/locate/yccog')]:
 r=d[0].insert_htmlbox(fitz.Rect(rect),html.escape(t),css="@font-face{font-family:cn;src:url('songti.ttf')}body{font-family:cn;font-size:7pt;margin:0}",archive=fitz.Archive(str(ROOT/'tmp/pdfs')),scale_low=1);assert r[0]>=0
out=ROOT/'output/pdf/029-线索类型与自传体记忆-中文原版式译本.pdf';d.save(out,garbage=4,deflate=True)
checks={'pages':len(d),'page_sizes_match':all(a.rect==b.rect for a,b in zip(d,src)),'doi_on_first_page':'10.1016/j.concog.2025.103983' in d[0].get_text(),'bibliography_unchanged':[],'numeric_tables':[]}
for pg,rect in [(14,[38,304,508,691]),(15,[38,49,508,548])]:checks['bibliography_unchanged'].append(src[pg].get_text(clip=fitz.Rect(rect))==d[pg].get_text(clip=fitz.Rect(rect)))
for pg,rect in [(5,[273,605,507,685]),(6,[227,87,507,133]),(6,[155,199,507,237]),(11,[99,587,507,675.3])]:
 pat=r'[-−]?\d+(?:\.\d+)?';a=re.findall(pat,src[pg].get_text(clip=fitz.Rect(rect)));b=re.findall(pat,d[pg].get_text(clip=fitz.Rect(rect)))
 checks['numeric_tables'].append({'page':pg+1,'count':len(a),'match':a==b})
assert checks['page_sizes_match'] and checks['doi_on_first_page'] and all(checks['bibliography_unchanged']) and all(x['match'] for x in checks['numeric_tables'])
(D/'最终排版核对.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2))
d[0].get_pixmap(matrix=fitz.Matrix(1.4,1.4)).save('/tmp/029-first-final.png')
print(out);print(checks)
