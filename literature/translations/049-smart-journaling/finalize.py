from pathlib import Path
import fitz,json,re,html,collections
R=Path(__file__).resolve().parents[3];H=Path(__file__).parent
row=next(x for x in json.loads((R/'literature/translations/全量精读翻译队列.json').read_text()) if x['number']==49)
O=fitz.open(R/row['source']);D=fitz.open(H/'049-原版式校对稿.pdf');A=[p for p in (H/'中文译稿-进行中.md').read_text().split('\n\n') if p and not p.startswith('<!--')]
for p in D:
 for r in p.search_for('DRAFT - tables and final QA pending'):p.add_redact_annot(r,fill=(1,1,1))
 p.apply_redactions(images=0,graphics=0)
D[12].add_redact_annot(fitz.Rect(319.8,573,537,637),fill=False)
D[12].apply_redactions(images=0,graphics=0)
D[0].add_redact_annot(fitz.Rect(210.2,443,549.7,465),fill=(.92,.92,.92));D[0].apply_redactions(images=0,graphics=0)
def ins(p,r,t,size):
 css=f"@font-face{{font-family:cn;src:url('songti.ttf')}}body{{margin:0;font-family:cn;font-size:{size}pt;line-height:1.25}}p{{margin:0 0 5pt 0}}"
 spare,scale=D[p].insert_htmlbox(fitz.Rect(r),''.join('<p>'+html.escape(v)+'</p>' for v in t.split('\n\n')),css=css,archive=fitz.Archive(str(R/'tmp/pdfs')),scale_low=.9)
 assert spare>=0,(p,spare)
ins(12,[319.8,574,537,637],'本文引用格式\n\n'+A[114],7.5)
ins(0,[210.2,443,549.7,465],A[6],7)
ins(12,[45.6,660,549.7,736],'''中文译本说明：Hutmacher、Schläger与Meerson（2023），Applied Cognitive Psychology，37：686–698。DOI：10.1002/acp.4033。

依据原作CC BY-NC 4.0许可制作，供非商业学习阅读。许可：https://creativecommons.org/licenses/by-nc/4.0/。修改包括中文翻译、字体及换行适配。保留13页、双栏、五张表的位置及原始人数；参考文献保留英文。AI翻译，未经作者审定。访谈引语由原作者从德语译成英语，本译本据英文转译。独立补充文件不在本篇13页原作范围内。''',7.3)
out=R/'output/pdf/049-智能日记应用与自传体记忆-中文原版式译本.pdf';D.save(out,garbage=4,deflate=True)
F=fitz.open(out);audit={'pages':len(F),'sizes_match':all(p.rect==O[i].rect for i,p in enumerate(F)),'draft_markers':sum('DRAFT' in p.get_text() for p in F),'table_counts':[],'missing_chinese':{}}
I=json.loads((H/'版面映射-进行中.json').read_text())+json.loads((H/'表格文字映射.json').read_text())
for i,p in enumerate(F):
 C=lambda t:collections.Counter(c for c in t if '\u4e00'<=c<='\u9fff');m=C(''.join(x['translation'] for x in I if x['page']==i))-C(p.get_text())
 if m:audit['missing_chinese'][i]=dict(m)
for pi,r in [(4,(200,80,220,250)),(4,(200,315,220,425)),(5,(200,80,220,178)),(6,(490,90,510,530))]:
 a=re.findall(r'\d+',O[pi].get_text(clip=fitz.Rect(r)));b=re.findall(r'\d+',F[pi].get_text(clip=fitz.Rect(r)));audit['table_counts'].append({'page':pi+1,'n':len(a),'equal':a==b})
assert audit['pages']==13 and audit['sizes_match'] and not audit['draft_markers'] and not audit['missing_chinese'] and all(x['equal'] for x in audit['table_counts'])
(H/'最终排版核对.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2));F[12].get_pixmap(matrix=fitz.Matrix(1.4,1.4)).save(R/'tmp/pdfs/049-final13.png');print(audit)
