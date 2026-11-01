from pathlib import Path
import fitz,json,html,re,collections
R=Path(__file__).resolve().parents[3];H=Path(__file__).parent
D=fitz.open(H/'054-原版式校对稿.pdf');O=fitz.open(R/'literature/sources/fulltext/E37-mediated-autobiographical-remembering-in.pdf')
for p in D:
 for r in p.search_for('DRAFT - tables and semantic/visual QA pending'):p.add_redact_annot(r,fill=(1,1,1))
 p.apply_redactions(images=0,graphics=0)
ref=D[11].search_for('References')[0];D[11].add_redact_annot(ref,fill=(1,1,1));D[11].apply_redactions(images=0,graphics=0)
# The online publication date is a raster object; cover only its occupied area.
D[11].draw_rect(fitz.Rect(56,645,250,656),fill=(1,1,1),color=None,overlay=True)
def ins(p,r,t,size):
 css=f"@font-face{{font-family:cn;src:url('songti.ttf')}}body{{margin:0;font-family:cn;font-size:{size}pt;line-height:1.35}}p{{margin:0 0 7pt 0}}"
 spare,scale=D[p].insert_htmlbox(fitz.Rect(r),''.join('<p>'+html.escape(s)+'</p>' for s in t.split('\n\n')),css=css,archive=fitz.Archive(str(R/'tmp/pdfs')),scale_low=.9)
 assert spare>=0,(p,t)
ins(11,[304.7,86,400,98],'参考文献',7)
ins(11,[56.7,645,292,659],'在线发表：2025年5月1日',7)
notes='''中文译本说明

原作：Hutmacher、Conrad、Appel与Schwan（2025），Cognitive Research: Principles and Implications，10:18。DOI：10.1186/s41235-025-00627-4。

本译本依据CC BY 4.0制作，完整许可见原刊首页；许可链接：https://creativecommons.org/licenses/by/4.0/。修改包括中文翻译、字体和换行适配。保留原刊13页、双栏、表格位置和英文参考文献。AI翻译，未经作者审定。

原文核对注：原刊第6、7页置信区间分别印为[t0.11, 0.51]和[t0.21, 0.59]，本译本照录，未擅自推定t为负号或更正统计值。第7页出现“internal resource”，按原文译为“内部资源”，上下文通常使用“内部过程”。

补充材料链接保留；独立补充文件不属于本篇13页正文。'''
ins(12,[304.7,530,540.9,740],notes,7.5)
out=R/'output/pdf/054-数字时代的媒介化自传体回忆-中文原版式译本.pdf';D.save(out,garbage=4,deflate=True)
F=fitz.open(out);audit={'pages':len(F),'sizes_match':all(p.rect==O[i].rect for i,p in enumerate(F)),'draft_markers':sum('DRAFT' in p.get_text() for p in F),'tables':[],'missing_chinese':{}}
items=json.loads((H/'版面映射-进行中.json').read_text())+json.loads((H/'表格文字映射.json').read_text())
for i,p in enumerate(F):
 C=lambda t:collections.Counter(c for c in t if '\u4e00'<=c<='\u9fff')
 missing=C(''.join(x['translation'] for x in items if x['page']==i))-C(p.get_text())
 if missing:audit['missing_chinese'][i+1]=dict(missing)
for pi,r in [(5,(420,110,541,275)),(7,(150,110,293,361)),(7,(150,450,293,523)),(8,(130,100,541,275))]:
 a=re.findall(r'\d+(?:\.\d+)?',O[pi].get_text(clip=fitz.Rect(r)));b=re.findall(r'\d+(?:\.\d+)?',F[pi].get_text(clip=fitz.Rect(r)));audit['tables'].append({'page':pi+1,'cells':len(a),'equal':a==b})
assert audit['sizes_match'] and audit['draft_markers']==0 and not audit['missing_chinese'] and all(x['equal'] for x in audit['tables'])
(H/'最终排版核对.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
for i in [11,12]:F[i].get_pixmap(matrix=fitz.Matrix(1.4,1.4)).save(R/f'tmp/pdfs/054-final-{i+1}.png')
print(out);print(audit)
