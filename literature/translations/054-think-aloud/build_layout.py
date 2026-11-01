"""054逐栏语义映射工作稿。表格保持原文，待独立回填与检查。页号为零基。"""
from pathlib import Path
import json,re,html
import fitz
ROOT=Path(__file__).resolve().parents[3]; HERE=Path(__file__).parent
D=fitz.open(ROOT/'literature/sources/fulltext/E37-mediated-autobiographical-remembering-in.pdf')
B={i:p.get_text('blocks') for i,p in enumerate(D)}
A=[p for p in (HERE/'中文译稿-进行中.md').read_text().split('\n\n') if p and not p.startswith('<!--')]
def join(*args):return '\n\n'.join(A[x] if isinstance(x,int) else x for x in args)
def cut(i,phrase):
 t=A[i];k=t.index(phrase);return t[:k],t[k:]
I=[]
def add(p,b,t,kind='body',rect=None):
 I.append(dict(page=p,block=b,source_rect=list(rect or B[p][b][:4]),source_text=B[p][b][4],translation=t,kind=kind))
a,b=cut(8,'该模型假定');add(0,6,join(7,a));add(0,7,b)
add(0,1,'原创研究论文','heading');add(0,2,A[0],'title');add(0,4,join(4,5),'abstract');add(0,5,A[6],'small');add(0,8,'开放获取','heading');add(0,9,A[111],'license');add(0,11,join(108,109,110),'small')
a,b=cut(11,'不过，');c,d=cut(14,'参与者在');add(1,1,join(9,10,a));add(1,2,join(b,12,13,c));add(2,1,d)
a,b=cut(17,'教育程度方面');add(2,2,join(15,16,a));add(2,3,b);add(2,4,join(18,19,20));add(3,1,join(21,22))
a,b=cut(24,'分析的上位类别');add(3,2,join(23,a));add(3,3,join(b,25))
a,b=cut(27,'（例如：“现在看到');add(3,4,join(26,a));add(4,1,b)
a,b=cut(28,'（c）');add(4,2,a);add(4,3,b);add(4,4,join(30,31))
a,b=cut(34,'例如，');add(4,5,join(32,33,a),rect=[304.7,398.1,540.9,724.3]);add(4,5,A[29],'footnote',rect=[56.7,705,292.9,729]);add(5,1,b)
add(5,2,join(35,36));a,b=cut(38,'因此，这些分析');add(5,3,join(37,a));add(5,4,b);add(5,5,join(39,40,41));add(5,20,A[42],'footnote')
a,b=cut(46,'和切换原因');add(5,6,join(45,a));add(6,1,b)
a,b=cut(48,'是否随事件类型');add(6,2,join(47,a));add(6,3,join(b,49));add(6,4,A[50],'footnote')
a,b=cut(52,'绝大多数参与者');add(7,1,join(51,a));add(7,2,b)
a,b=cut(61,'此外，');add(7,3,join(59,60,a));add(8,1,b);add(8,2,join(64,65));add(8,3,join(66,67))
a,b=cut(69,'一方面，');add(8,4,join(68,a));add(9,1,join(b,70,71))
a,b=cut(73,'回忆重要日期和随机日期时');add(9,2,join(72,a));add(10,1,b);add(10,2,join(74,75,76));add(10,3,A[77]);add(10,4,join(78,79));add(11,1,join(80,81))
for block,ids in [(2,[82]),(3,[83]),(4,[84]),(5,[85,86]),(6,[87,88]),(7,[89,90]),(8,[91,92]),(9,[93]),(10,[94,95]),(11,[96,97]),(12,[98,99]),(13,[100])]:add(11,block,join(*ids),'small')
add(12,3,join(103,104),'small')
# Redact all originals before inserting any replacement (merged block 4/5 contains a footnote).
for x in I:D[x['page']].add_redact_annot(fitz.Rect(x['source_rect']),fill=(1,1,1))
for p in D:p.apply_redactions(images=0,graphics=0)
font=ROOT/'tmp/pdfs/songti.ttf'
for x in I:
 r=fitz.Rect(x['source_rect']);r.y1+=1
 if x['kind'] in ['small','footnote','license']:r.x1=540.9 if r.x0>300 else (534.1 if x['kind']=='license' else 292.9)
 size={'body':10.5,'abstract':10,'heading':10,'title':19,'small':7.5,'footnote':7,'license':6.5}[x['kind']]
 if x['kind']=='small' and r.height<14:r.y1+=3
 def render(t):
  out=[]
  for v in t.split('\n\n'):
   head=v.startswith('#');v=re.sub(r'^#+ ','',v)
   v=html.escape(v);v=re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',v)
   v=v.replace('ω²ₚ','ω<sup>2</sup><sub>p</sub>')
   out.append(('<h3>' if head else '<p>')+v+('</h3>' if head else '</p>'))
  return ''.join(out)
 css=f"@font-face{{font-family:cn;src:url('{font.name}')}}body{{margin:0;font-family:cn;font-size:{size}pt;line-height:1.42}}p{{margin:0 0 5pt 0}}h3{{font-size:1.03em;margin:0 0 4pt 0;font-weight:bold}}"
 spare,scale=D[x['page']].insert_htmlbox(r,render(x['translation']),css=css,archive=fitz.Archive(str(font.parent)),scale_low=.7)
 x.update(target_rect=list(r),font_size=size*scale,spare_height=spare)
 if spare<0:raise ValueError(('overflow',x['page'],x['block']))
for p in D:p.insert_text((56,770),'DRAFT - tables and semantic/visual QA pending',fontsize=7,color=(.65,0,0))
D.save(HERE/'054-原版式工作稿.pdf',deflate=True,garbage=4)
(HERE/'版面映射-进行中.json').write_text(json.dumps(I,ensure_ascii=False,indent=2))
print('pages',len(D),'regions',len(I),'min font',min(x['font_size'] for x in I))
print('small body regions',[(x['page'],x['block'],round(x['font_size'],1)) for x in I if x['kind']=='body' and x['font_size']<9])
