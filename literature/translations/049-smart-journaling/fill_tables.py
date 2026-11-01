from pathlib import Path
import fitz,json,html
R=Path(__file__).resolve().parents[3];H=Path(__file__).parent
D=fitz.open(H/'049-原版式工作稿.pdf');A=[p for p in (H/'中文译稿-进行中.md').read_text().split('\n\n') if p and not p.startswith('<!--')];I=[]
def add(p,r,t,size=7.5):I.append(dict(page=p,source_rect=r,translation=t,size=size))
def rows(i):return [[v.strip() for v in l.strip('|').split('|')] for l in A[i].splitlines()[2:]]
# Keep all numerical cells, striped fills and rules from the source PDF.
for p,title,note,ytitle,ynote in [(4,31,33,51,255),(4,37,39,285,433),(5,48,50,51,185),(6,57,59,51,535),(7,68,70,51,328)]:
 w=550 if p==6 else 288.5
 add(p,[45.6,ytitle,w,ytitle+12],A[title].replace('**',''),8)
 h=50 if p==5 else 43 if p==7 else 13
 add(p,[45.6,ynote,w,ynote+h],A[note],7)
for p,idx,start,heady in [(4,32,84,69),(4,38,318,303),(5,49,84,69)]:
 add(p,[52.6,heady,195,heady+12],'记忆活动' if p==5 else '功能' if idx==32 else '内容')
 add(p,[204,heady,282,heady+12],'参与者人数')
 for i,row in enumerate(rows(idx)):
  y=start+i*14;add(p,[52.6,y,200,y+12],row[0])
# Table 4: quotations remain in their individual original rows.
add(6,[52.6,69,150,89],'类别');add(6,[156,69,485,89],'示例');add(6,[492,69,542,89],'参与者人数')
ys=[94.5,108.5,143.5,168,203,238,262.5,287,311.5,325.5,339.5,374.5,409.5,434,469,483,518]
rr=rows(58);assert len(rr)==len(ys)
for i,(row,y) in enumerate(zip(rr,ys)):
 end=ys[i+1]-2 if i+1<len(ys) else 529
 add(6,[52.6,y,150,end],row[0],7.4)
 if row[1]:add(6,[155.8,y,485,end],row[1],7.4)
# Table 5 leaves original app names, rewrites descriptions.
add(7,[52.6,69,105,81],'应用');add(7,[109.7,69,282,81],'简介')
for row,y,end in zip(rows(69),[84,171.5,248.5],[167,244,322]):add(7,[109.6,y,283,end],row[1],7.5)
for x in I:D[x['page']].add_redact_annot(fitz.Rect(x['source_rect']),fill=False)
for p in D:p.apply_redactions(images=0,graphics=0)
for x in I:
 css=f"@font-face{{font-family:cn;src:url('songti.ttf')}}body{{margin:0;font-family:cn;font-size:{x['size']}pt;line-height:1.12}}p{{margin:0}}"
 spare,scale=D[x['page']].insert_htmlbox(fitz.Rect(x['source_rect']),'<p>'+html.escape(x['translation'])+'</p>',css=css,archive=fitz.Archive(str(R/'tmp/pdfs')),scale_low=.85)
 assert spare>=0,(x,spare)
 x['font_size']=x['size']*scale
D.save(H/'049-原版式校对稿.pdf',garbage=4,deflate=True)
(H/'表格文字映射.json').write_text(json.dumps(I,ensure_ascii=False,indent=2))
print('table regions',len(I),'minimum font',min(x['font_size'] for x in I))
for i in [4,5,6,7]:D[i].get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(R/f'tmp/pdfs/049-tables-{i+1}.png')
