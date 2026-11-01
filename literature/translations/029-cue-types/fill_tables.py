from pathlib import Path
import fitz,json,html,re
ROOT=Path(__file__).resolve().parents[3];D=Path(__file__).parent
P=(D/'中文译稿-进行中.md').read_text().split('\n\n')
src=fitz.open(next((ROOT/'literature/sources/fulltext').glob('029-*.pdf')))
doc=fitz.open(ROOT/'output/pdf/029-线索类型与自传体记忆-中文排版草稿.pdf')
R=[]
def add(p,rect,t,size=7):R.append(dict(page=p,rect=rect,text=t,size=size))
def table(i):return [[s.strip() for s in line.strip('|').split('|')] for line in P[i].splitlines()[2:]]
def labels(p,rect,strings,ys,size=6.8):
 for t,y in zip(strings,ys):add(p,[rect[0],y,rect[1],y+8.57],t,size)
# Captions: two original lines combined in same area.
for p,rect,i in [(5,[101,555.8,507,578],49),(6,[69.5,50.5,507,73],51),(6,[39,154,507,177],53),(10,[39,491.7,507,515],73),(11,[39,537.6,507,561],75),(12,[39,50.5,507,73],87)]:add(p,rect,re.sub(r'^#+ ','',P[i]),8)
add(5,[274,579.4,380,591],'均值（标准差）');add(5,[274,592.5,380,605],'年轻人');add(5,[398,592.5,507,605],'老年人')
labels(5,[107,270],[r[0] for r in table(50)],[605.7+j*8.57 for j in range(9)])
add(6,[227,74,380,86.8],'情景性自传体记忆（n = 1406）',6.8);add(6,[384,74,507,86.8],'非情景性记忆（n = 1091）',6.8)
labels(6,[75,225],[r[0] for r in table(52)],[87.3+j*8.57 for j in range(5)])
add(6,[155,177.8,355,186.5],'情景性自传体记忆',6.8);add(6,[360,177.8,507,186.5],'非情景性自传体记忆',6.8)
for x,t in [(155,'年轻人'),(258,'老年人'),(360,'年轻人'),(462,'老年人')]:add(6,[x,186.4,x+45,198],t,6.8)
labels(6,[45,150],[r[0] for r in table(54)],[199.5+j*8.57 for j in range(4)])
# Table 4 keeps original three columns and row boundaries.
for x,x1,t in [(60,210,'问题'),(214,251,'主题'),(254,507,'来源／参考文献')]:add(10,[x,515.4,x1,528.6],t,7)
ys=[528.6,545.75,562.9,580.05,597.2,614.35,631.5,648.6,665.75,674.3,685]
for row,y,y1 in zip(table(74),ys,ys[1:]):
 for t,x,x1 in zip(row,[60,214,254],[210,251,507]):add(10,[x,y,x1,y1],t,6.7)
# Numeric table: retain every original numeric cell.
for x,t in zip([100,180.3,270.2,360.2,441.4],['词语','句子','问题','照片','视频']):add(11,[x,561.3,x+38,573],t)
for x in [100,180.3,270.2,360.2,441.4]:add(11,[x,574.4,x+30,587],'均值')
labels(11,[45,98],[r[0] for r in table(76)],[587.55+j*8.57 for j in range(10)])
add(11,[39,675.3,507,691],P[77],7)
# Table 6: individual semantic rows; same positions, bullets restored.
add(12,[45,74,230,87.3],'线索内容');add(12,[234,74,507,87.3],'提取率与记忆特征')
ys=[87.3,130.15,173.0,207.3,250.15,275.85,293.0,327.25,370.05,387.2,416]
for row,y,y1 in zip(table(88),ys,ys[1:]):
 add(12,[45,y,230,y1],row[0],7)
 add(12,[234,y,507,y1],'\n'.join('• '+s for s in row[1].rstrip('。').split('；')),6.9)
add(12,[39,417.5,507,440],P[89],7.2)
# Redact whole text areas while keeping vector lines and stripes.
for r in R:doc[r['page']].add_redact_annot(fitz.Rect(r['rect']),fill=False)
for p in doc:p.apply_redactions(images=0,graphics=0)
for r in R:
 css="@font-face{font-family:cn;src:url('songti.ttf')}body{font-family:cn;font-size:%spt;margin:0;padding:0;line-height:1.05}"%r['size']
 spare,scale=doc[r['page']].insert_htmlbox(fitz.Rect(r['rect']),html.escape(r['text']).replace('\n','<br>'),css=css,archive=fitz.Archive(str(ROOT/'tmp/pdfs')),scale_low=.8)
 r.update(spare=spare,scale=scale)
 if spare<0:raise RuntimeError(r)
out=ROOT/'output/pdf/029-线索类型与自传体记忆-表格排版草稿.pdf';doc.save(out,garbage=4,deflate=True)
(D/'表格文字映射.json').write_text(json.dumps(R,ensure_ascii=False,indent=2))
print(out);print('regions',len(R),'min scale',min(r['scale'] for r in R))
