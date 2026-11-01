"""049语义分栏工作稿；表格另行回填。页索引从0起。"""
from pathlib import Path
import fitz,json,re,html
R=Path(__file__).resolve().parents[3];H=Path(__file__).parent
row=next(x for x in json.loads((R/'literature/translations/全量精读翻译队列.json').read_text()) if x['number']==49)
D=fitz.open(R/row['source'])
A=[p for p in (H/'中文译稿-进行中.md').read_text().split('\n\n') if p and not p.startswith('<!--')]
def j(*xs):return '\n\n'.join(A[x] if isinstance(x,int) else x for x in xs)
def cut(i,k):
 t=A[i];n=t.index(k);return t[:n],t[n:]
I=[]
def add(p,side,t,y0=52,y1=738,kind='body',rect=None):
 r=rect or ([45.6,y0,288.5,y1] if side==0 else [306.8,y0,549.7,y1])
 I.append(dict(page=p,source_rect=r,translation=t,kind=kind,source_text=D[p].get_text(clip=fitz.Rect(r))))
a,b=cut(8,'此后，');c,d=cut(9,'人类记忆会');add(0,0,j(7,a),492,700);add(0,1,j(b,c),492,700)
a,b=cut(10,'或避免想起');c,e=cut(12,'一种方法是');add(1,0,j(d,a));add(1,1,j(b,11,c))
a,b=cut(16,'即定性研究');add(2,0,j(e,13,14,15,a));c,d=cut(20,'参与者被要求');add(2,1,j(b,17,18,19,c));add(3,0,j(d,21,22))
a,b=cut(30,'大多数还');add(3,1,j(23,24,25,26,27,28,29,a));c,d=cut(35,'第三，');add(4,0,j(b,34,c),468,738)
a,b=cut(44,'具体而言，');add(4,1,j(d,36,40,41,42,43,a));c,d=cut(45,'以检验这些');add(5,0,j(b,c),260,738);add(5,1,j(d,46,47,51,52,53,54))
a,b=cut(56,'从而面临');add(6,0,j(55,a),559,738);c,d=cut(61,'这些访谈');add(6,1,j(b,60,c),559,738)
a,b=cut(65,'研究邀请');add(7,0,j(d,62,63,64,a),403,738);c,d=cut(72,'编码手册');add(7,1,j(b,66,67,71,c))
a,b=cut(79,'所有长期用户');add(8,0,j(d,73,74,75,76,77,78,a));c,d=cut(83,'所有长期用户都报告');add(8,1,j(b,80,81,82,c))
a,b=cut(89,'这些陈述');add(9,0,j(d,84,85,86,87,88,a));c,d=cut(91,'研究1中');add(9,1,j(b,90,c))
a,b=cut(94,'在这一背景下');add(10,0,j(d,92,93,a));c,d=cut(96,'而影响强度');add(10,1,j(b,95,c));add(11,0,j(d,97),52,352)
for ids,y0,y1 in [([98,99],364,416),([100,101],429,455),([102,103],468,497),([104,105],507,537),([106,107,108],546,670)]:add(11,0,j(*ids),y0,y1,'small')
add(11,0,'参考文献',678,690,'small')
add(12,1,j(111,112),515,554,'small');add(12,1,'本文引用格式',574,586,'small',rect=[319.8,574,405,586])
# First-page identity and abstract.
add(0,0,A[116],kind='small',rect=[45.6,70,190,83]);add(0,0,A[0],kind='title',rect=[45.6,110,549.7,157]);add(0,0,A[117],kind='small',rect=[45.6,215,192,237]);add(0,0,A[118],kind='small',rect=[45.6,245,192,300]);add(0,0,j(4,5),kind='abstract',rect=[210.2,222,549.7,430]);add(0,0,A[6],kind='small',rect=[210.2,443,549.7,464]);add(0,0,j(120,121),kind='license',rect=[45.6,711,549.7,742])
# Header metadata kept separate from DOI.
for q in ['Received: 27 June 2022','Revised: 6 October 2022','Accepted: 15 December 2022']:
 for r in D[0].search_for(q):D[0].add_redact_annot(r,fill=(1,1,1))
add(0,0,A[119],kind='license',rect=[45.6,30,450,39])
for x in I:
 fill=(.92,.92,.92) if x['page']==0 and x['kind']=='abstract' else (1,1,1)
 D[x['page']].add_redact_annot(fitz.Rect(x['source_rect']),fill=fill)
for p in D:p.apply_redactions(images=0,graphics=0)
for x in I:
 size={'body':10,'title':17,'abstract':10,'small':7,'license':6}[x['kind']];r=fitz.Rect(x['source_rect']);r.y1+=1
 out=[]
 for t in x['translation'].split('\n\n'):
  head=t.startswith('#');t=re.sub('^#+ ','',t);t=html.escape(t)
  out.append(('<h3>' if head else '<p>')+t+('</h3>' if head else '</p>'))
 css=f"@font-face{{font-family:cn;src:url('songti.ttf')}}body{{margin:0;font-family:cn;font-size:{size}pt;line-height:1.4}}p{{margin:0 0 5pt 0}}h3{{font-size:1.02em;margin:0 0 5pt 0}}"
 spare,scale=D[x['page']].insert_htmlbox(r,''.join(out),css=css,archive=fitz.Archive(str(R/'tmp/pdfs')),scale_low=.75)
 x.update(target_rect=list(r),font_size=size*scale,spare_height=spare)
 if spare<0:raise ValueError((x['page'],x['source_rect']))
for p in D:p.insert_text((45,749),'DRAFT - tables and final QA pending',fontsize=6,color=(.7,0,0))
D.save(H/'049-原版式工作稿.pdf',garbage=4,deflate=True)
(H/'版面映射-进行中.json').write_text(json.dumps(I,ensure_ascii=False,indent=2))
print('regions',len(I),'small body',[(x['page'],x['font_size']) for x in I if x['kind']=='body' and x['font_size']<9])
