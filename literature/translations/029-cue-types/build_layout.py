from pathlib import Path
import fitz,json,re,html
ROOT=Path(__file__).resolve().parents[3]
D=Path(__file__).parent
P=(D/'中文译稿-进行中.md').read_text().split('\n\n')
B=json.loads((D/'原文文字块.json').read_text())
regions=[]
def split(i,phrase):
 t=P[i]; k=t.index(phrase);return t[:k],t[k:]
def add(page,ids,text,size=9.5,rect=None):
 boxes=[B[page][i]['bbox'] for i in ids]
 if rect is None:rect=[min(b[0] for b in boxes),min(b[1] for b in boxes),507.6,max(b[3] for b in boxes)+1]
 regions.append(dict(page=page,blocks=ids,source_rects=boxes,target_rect=rect,translation=text,font_size=size,source_text='\n'.join(B[page][i]['text'] for i in ids)))
def group(*items):return '\n\n'.join(P[x] if isinstance(x,int) else x for x in items)
a,b=split(8,'尽管某项自传体记忆测验')
c,d=split(12,'此外，流行音乐')
e,f=split(19,'（18—30岁')
g,h=split(28,'其任务是')
i,j=split(35,'老年组680条')
k,l=split(43,'分别对数据子集')
m,n=split(44,'全部反应与情景性反应')
n,o=n.split('对于词语线索，'); n+='对于词语线索，'
# Place word subtype contrast on page 9; no content removed.
u,v=split(45,'为考虑量表')
w,x=split(63,'样本中，24%')
y,z=split(70,'及童年')
aa,ab=split(80,'另一方面，')
ac,ad=split(83,'也符合较新的观点')
ae,af=split(91,'希望这一描述性资源')
add(0,[0],'研究论文',10, [39,141,200,157])
add(0,[1],P[0].lstrip('# '),16,[39,158,507,215])
add(0,[3],'英国利兹大学心理学院\n英国约克大学心理学系',8,[39,242,507,266])
add(0,[4],'文章信息',9,[39,283,180,298]);add(0,[5],P[6].replace('；','\n'),8,[39,303,185,375])
add(0,[6],'摘要',10,[197,283,507,298]);add(0,[7],P[5],9,[197,303,507,493])
add(0,[8,9],group(7,a),9.3,[39,511,507,601])
add(1,list(range(5)),group(b,9,10,11,c),9.5)
add(2,list(range(8)),group(d,13,14,15,16,17,18,e),9.5)
add(3,list(range(10)),group(f,*range(20,28),g),9.5)
add(4,list(range(6)),group(h,29,31,32,33,34,i),9.5)
add(4,[6],P[30],7.5)
add(5,list(range(9)),group(j,36,37,38,39,40,41,42,k),9.5)
add(6,[0,1],group(l,m),9.0)
add(7,[0],n,9.0)
add(8,[0,1],group(o,u),9.0)
add(9,list(range(8)),group(v,46,47,48,60,61,62,w),9.5)
add(10,list(range(8)),group(x,64,65,66,67,68,69,y),9.3)
add(11,list(range(5)),group(z,71,72,78,79,aa),9.4)
add(12,list(range(4)),group(ab,81,82,ac),9.4)
add(13,list(range(6)),group(ad,84,85,86,90,ae),9.4)
add(14,list(range(10)),group(af,*range(92,101)),9.4)
for page,bid,pi in [(6,8,56),(7,1,57),(8,2,58),(8,3,59)]:add(page,[bid],P[pi],7.8)
# Preserve bibliography and original journal mastheads. Tables and raster figure labels are completed in a subsequent pass.
src=next((ROOT/'literature/sources/fulltext').glob('029-*.pdf'));doc=fitz.open(src)
for r in regions:
 for box in r['source_rects']:doc[r['page']].add_redact_annot(fitz.Rect(box),fill=False)
for page in doc:page.apply_redactions(images=0,graphics=0)
archive=fitz.Archive(str(ROOT/'tmp/pdfs'))
for r in regions:
 paras=[]
 for t in r['translation'].split('\n\n'):
  heading=t.startswith('#');t=re.sub(r'^#+\s*','',t);t=html.escape(t);t=re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',t)
  paras.append(('<p class="heading">' if heading else '<p>')+t.replace('\n','<br>')+'</p>')
 css="@font-face{font-family:cn;src:url('songti.ttf')}body{font-family:cn;margin:0;padding:0;font-size:%spt}p{margin:0 0 3pt;line-height:1.3}p.heading{font-weight:bold;margin:5pt 0}"%r['font_size']
 spare,scale=doc[r['page']].insert_htmlbox(fitz.Rect(r['target_rect']),''.join(paras),css=css,archive=archive,scale_low=.75)
 r['spare_height']=spare;r['scale']=scale;r['effective_font_size']=scale*r['font_size']
 if spare<0:raise RuntimeError(('overflow',r['page'],r['blocks']))
output=ROOT/'output/pdf/029-线索类型与自传体记忆-中文排版草稿.pdf';output.parent.mkdir(exist_ok=True,parents=True)
doc.save(output,garbage=4,deflate=True)
(D/'版面映射-进行中.json').write_text(json.dumps(regions,ensure_ascii=False,indent=2))
print(output);print('regions',len(regions),'min font',min(r['effective_font_size'] for r in regions))
