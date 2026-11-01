from pathlib import Path
import fitz,json,re,html
from fontTools import subset
ROOT=Path(__file__).resolve().parents[3];D=Path(__file__).parent
P=(D/'中文译稿-进行中.md').read_text().split('\n\n');B=json.loads((D/'原文文字块.json').read_text());R=[]
def g(*a):return '\n\n'.join(P[x].strip() if isinstance(x,int) else x for x in a)
def cut(i,s):
 k=P[i].index(s);return P[i][:k],P[i][k:]
def add(p,rect,t,size=10):R.append(dict(page=p,rect=rect,text=t,size=size))
def block(p,b,t,size=10):
 r=B[p][b]['bbox'];x=54 if r[0]<300 else 317
 add(p,[x,r[1]-1,298 if x==54 else 561,r[3]+2],t,size)
a,b=cut(9,'以及由此延伸的')
c,d=cut(11,'后一种情况')
e,f=cut(16,'因此，非自主记忆')
h,i=cut(26,'原因是什么')
j,k=cut(39,'定性主题分析')
l,m=cut(46,'40%涉及一般事件')
n,o=cut(53,'与其他人有关')
q,r=cut(61,'而数字的东西')
s,t=cut(67,'唤回记忆的往往')
u,v=cut(83,'回答表明')
w,x=cut(90,'可以事先明确询问')
y,z=cut(94,'我们认为，一个十分重要的问题')
aa,ab=cut(99,'通过位置操作')
add(0,[54,60,561,105],P[0],17)
# Preserve author names and affiliation markers; translate the affiliation lines only.
add(0,[54,126,298,182],'悉尼科技大学\n设计、建筑与建造学院\ndomenique.vangennip@uts.edu.au\nelise.vandenhoven@uts.edu.au',8.5)
add(0,[317,126,561,182],'荷兰埃因霍温理工大学\n工业设计系\np.markopoulos@tue.nl',9)
add(0,[54,195,298,414],g(4,5));block(0,8,P[6],9);block(0,9,P[7],9)
block(0,10,g(8,a));block(0,11,b);add(0,[317,531,561,554],P[10],8)
block(0,14,c);add(0,[54,622,298,644],'作者最终稿，出版标识已省略。\nhttp://dx.doi.org/10.1145/2702123.2702460',7.5)
block(1,1,d);block(1,2,P[12]);block(1,3,P[13]);block(1,4,P[14]);block(1,5,g(15,e));block(1,6,f);block(1,7,P[17]);block(1,8,g(18,19));block(1,9,P[20])
block(2,1,g(21,22));block(2,2,P[23]);block(2,3,g(24,25));block(2,4,h);block(2,5,i);block(2,6,P[27]);block(2,7,g(28,29));block(2,8,g(30,31));block(2,9,g(32,33))
block(3,1,P[34]);block(3,2,P[35],8);block(3,3,g(36,37));block(3,4,g(38,j));block(3,5,k);block(3,6,P[40]);block(3,7,g(41,42));block(3,8,P[43]);block(3,9,g(44,45));block(3,10,l)
block(4,1,g(m,47))
left=P[49].split('\n- ')[1:];right=P[50].split('\n- ')[1:]
for bid,txt in zip([2,4,6],left):
 rr=B[4][bid]['bbox'];add(4,[54,rr[1]-1,199,rr[3]+2],txt,9)
for bid,txt in zip([3,5,7],right):
 rr=B[4][bid]['bbox'];add(4,[208,rr[1]-1,298,rr[3]+4],txt,9)
block(4,8,P[48],8);block(4,9,g(51,52));block(4,10,n);block(4,11,o);block(4,12,g(54,55));block(4,13,g(56,57));block(4,14,g(58,59));block(4,15,g(60,q),9)
block(5,1,r);block(5,2,P[62]);block(5,3,g(63,64));block(5,4,P[65]);block(5,5,g(66,s));block(5,6,t);block(5,7,P[68]);block(5,8,g(69,70));block(5,9,g(71,72))
block(6,1,P[73]);block(6,2,P[74]);block(6,3,P[75]);block(6,4,g(76,77));block(6,5,P[78]);block(6,6,P[79]);block(6,7,P[80]);block(6,8,P[81]);block(6,9,P[82]);block(6,10,u)
block(7,1,v);block(7,2,P[84]);block(7,3,P[85]);block(7,4,g(86,87));block(7,5,P[88]);block(7,6,g(89,w));block(7,7,x);block(7,8,P[91]);block(7,9,P[92]);block(7,10,g(93,y))
block(8,1,z);block(8,2,P[95]);block(8,3,P[96]);block(8,4,g(97,98));block(8,5,aa);block(8,6,ab);block(8,7,g(100,101));block(8,8,g(102,103));block(8,9,P[104]);block(8,10,P[105]);block(9,1,g(106,107))
add(9,[54,146,298,158],P[108],9)
add(0,[54,662,298,714],'译本说明：AI中文翻译，未经作者审定，用于个人阅读。保留原作双栏、图表位置与参考文献题录；理论及技术评价按2015年原作理解。',8)
font=ROOT/'tmp/pdfs/028-songti.ttf';opt=subset.Options();ff=subset.load_font(str(ROOT/'tmp/pdfs/songti.ttf'),opt);sub=subset.Subsetter(options=opt);sub.populate(text=''.join(a['text'] for a in R));sub.subset(ff);subset.save_font(ff,str(font),opt)
doc=fitz.open(ROOT/'literature/sources/fulltext/06-things-that-make-us-reminisce-2015.pdf')
for a in R:
 a['source_text']=doc[a['page']].get_text(clip=fitz.Rect(a['rect']));doc[a['page']].add_redact_annot(fitz.Rect(a['rect']),fill=False)
for p in doc:p.apply_redactions(images=0,graphics=0)
for a in R:
 ps=[]
 for t in a['text'].split('\n\n'):
  head=t.startswith('#');t=re.sub(r'^#+\s*','',t.strip());t=html.escape(t);t=re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',t)
  ps.append(('<p class="head">' if head else '<p>')+t.replace('\n','<br>')+'</p>')
 css="@font-face{font-family:cn;src:url('028-songti.ttf')}body{font-family:cn;font-size:%spt;margin:0}p{margin:0 0 3pt;line-height:1.2}.head{font-weight:bold;margin-bottom:3pt}"%a['size']
 spare,scale=doc[a['page']].insert_htmlbox(fitz.Rect(a['rect']),''.join(ps),css=css,archive=fitz.Archive(str(ROOT/'tmp/pdfs')),scale_low=.8)
 a.update(spare=spare,scale=scale)
 if spare<0:raise RuntimeError((a['page'],a['rect'],a['text'][:40]))
out=ROOT/'output/pdf/028-日常记忆线索-中文排版草稿.pdf';doc.save(out,garbage=3,deflate=True);doc.close()
(D/'版面映射-进行中.json').write_text(json.dumps(R,ensure_ascii=False,indent=2))
print(out,'regions',len(R),'minscale',min(a['scale'] for a in R))
doc=fitz.open(out)
for i in range(len(doc)):doc[i].get_pixmap(matrix=fitz.Matrix(1.35,1.35)).save('/tmp/028-qa-%s.png'%i)
