from pathlib import Path
import fitz,json,re,html
from fontTools import subset
ROOT=Path(__file__).resolve().parents[3];D=Path(__file__).parent
P=(D/'中文译稿-进行中.md').read_text().split('\n\n'); B=json.loads((D/'原文文字块.json').read_text());R=[]
def g(*a):return '\n\n'.join(P[x].strip() if isinstance(x,int) else x for x in a)
def cut(i,s):
 k=P[i].index(s);return P[i][:k],P[i][k:]
def add(p,rect,t,size=10):R.append(dict(page=p,rect=rect,text=t,size=size))
def block(p,b,t,size=10):
 r=B[p][b]['bbox'];x=51 if r[0]<300 else 306
 add(p,[x,r[1]-1,289 if x==51 else 544,r[3]+3],t,size)
def head(p,b,i):block(p,b,P[i].strip(),10)
a,b=cut(8,'她很可能') if '她很可能' in P[8] else cut(8,'很可能')
c,d=cut(12,'情景记忆')
e,f=cut(19,'人类记忆系统')
h,i=cut(25,'或保持相对独特')
j,k=cut(31,'是否与记忆搜索')
l,m=cut(37,'包括状态依赖效应')
n,o=cut(49,'Teddy 是')
q,r=cut(55,'使用痕迹')
s,t=cut(63,'桌子内部')
u,v=cut(73,'5. 在任何时候')
w,x=cut(107,'实际发生之事')
y,z=cut(113,'文字就应是')
add(0,[57,65,220,80],'研究论文',9)
add(0,[51,105,544,145],P[0],17)
add(0,[51,243,544,268],'收稿：2005年10月3日／接受：2006年9月1日／在线发表：2007年7月17日\n© Springer-Verlag London Limited 2007',8)
block(0,4,g(4,5));block(0,5,P[6],9);head(0,6,7);block(0,7,a)
block(0,8,g(b,9));head(0,9,10);block(0,10,g(11,c))
block(0,11,'E. van den Hoven（通讯作者）\n埃因霍温理工大学工业设计系\nDen Dolech 2，HG 2.53，P.O. Box 513\n5600 MB 埃因霍温，荷兰\n电子邮箱：E.v.d.Hoven@tue.nl',7.5)
block(0,12,'B. Eggen\n埃因霍温理工大学工业设计系\nDen Dolech 2，HG 2.39，P.O. Box 513\n5600 MB 埃因霍温，荷兰',7.5)
block(1,0,g(d,13));head(1,1,14);block(1,2,P[15]);block(1,3,P[16]);block(1,4,P[17]);head(1,5,18);block(1,6,e)
block(1,7,g(f,20));head(1,8,21);block(1,9,g(22,23,24,h))
block(2,0,g(i,26));head(2,1,27);block(2,2,P[28]);block(2,3,P[29]);block(2,4,g(30,j));block(2,5,k);head(2,6,32);block(2,7,g(33,34,35,36,l))
block(3,0,g(m,38));head(3,1,39);block(3,2,P[40]);head(3,3,41);block(3,4,P[42]);head(3,5,43);block(3,6,P[44]);head(3,7,45);block(3,8,g(46,47,48,n))
block(4,0,g(o,50));head(4,1,51);block(4,2,g(52,53));head(4,3,54);block(4,4,q);block(4,5,g(r,56));head(4,6,57);block(4,7,g(58,59,60,61,62,s));block(4,8,P[75].replace('**脚注1。**','1'),7.5)
block(5,0,g(t,64,65,66,67));block(5,1,g(68,69,70,71,72));block(5,2,u)
add(5,[51,58,166,116],'表1  增强记忆系统按本文介绍顺序排列，并根据其支持的媒体类型分类。',8)
for xx,word in [(316,'照片'),(367,'文字'),(413,'声音'),(466,'视频'),(517,'物件')]:add(5,[xx,62,xx+29,75],word,8)
add(5,[179,208,313,220],'物件扫描仪 [42]',8)
block(6,0,v);head(6,1,76);block(6,2,g(77,78,79));head(6,3,81);block(6,4,P[82]);block(6,5,P[83]);block(6,6,P[84]);head(6,7,85);block(6,8,g(86,87,88));block(6,9,P[80].replace('**脚注2。**','2'),7.5)
block(7,0,P[89]);head(7,1,90);block(7,2,g(91,92,93));block(7,3,g(94,95,96));block(7,4,P[97]);add(7,[306,593,544,719],P[98]);add(7,[51,696,289,719],P[99],7.5)
head(8,0,100);block(8,1,P[101]);block(8,2,P[102]);block(8,3,P[103]);block(8,4,P[104]);block(8,5,g(105,106));block(8,6,w.replace('**',''));block(8,7,x.replace('**',''));block(8,8,P[108]);block(8,9,P[109]);block(8,10,P[110]);block(8,11,P[111]);block(8,12,g(112,y))
block(9,0,g(z,114));head(9,1,115);block(9,2,g(116,117));block(9,3,g(118,119),8);head(9,4,120)
add(10,[306,650,544,714],'译本说明：AI中文翻译，未经作者审定。用于个人阅读。原作发表于2008年，理论与技术评价按原作历史时点理解；参考文献及照片中的设备界面保留原文。DOI：10.1007/s00779-007-0177-9。',8)
# Keep footnote text below the original separator rule.
for a in R:
 if (a['page']==4 and a['text'].startswith('1 可')) or (a['page']==6 and a['text'].startswith('2 在')): a['rect'][1]+=5
# Subset only the newly added Chinese font before embedding; leave original PDF fonts intact.
font=ROOT/'tmp/pdfs/016-songti.ttf'; opt=subset.Options();f=subset.load_font(str(ROOT/'tmp/pdfs/songti.ttf'),opt);sub=subset.Subsetter(options=opt);sub.populate(text=''.join(x['text'] for x in R));sub.subset(f);subset.save_font(f,str(font),opt)
doc=fitz.open(ROOT/'literature/sources/fulltext/02-van-den-hoven-eggen-2008-augmented-memory-am-theory.pdf')
for a in R:
 a['source_text']=doc[a['page']].get_text(clip=fitz.Rect(a['rect']));doc[a['page']].add_redact_annot(fitz.Rect(a['rect']),fill=False)
for p in doc:p.apply_redactions(images=0,graphics=0)
for a in R:
 ps=[]
 for t in a['text'].split('\n\n'):
  t=re.sub(r'^#+\s*','',t.strip());t=html.escape(t);t=re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',t);ps.append('<p>'+t.replace('\n','<br>')+'</p>')
 css="@font-face{font-family:cn;src:url('016-songti.ttf')}body{font-family:cn;font-size:%spt;margin:0}p{margin:0 0 4pt;line-height:1.25}"%a['size']
 spare,scale=doc[a['page']].insert_htmlbox(fitz.Rect(a['rect']),''.join(ps),css=css,archive=fitz.Archive(str(ROOT/'tmp/pdfs')),scale_low=.75)
 a.update(spare=spare,scale=scale)
 if spare<0:raise RuntimeError((a['page'],a['rect'],a['text'][:40]))
out=ROOT/'output/pdf/016-自传体记忆理论与增强记忆设计-中文排版草稿.pdf';doc.save(out,garbage=3,deflate=True)
(D/'版面映射-进行中.json').write_text(json.dumps(R,ensure_ascii=False,indent=2))
print(out,'regions',len(R),'minscale',min(a['scale'] for a in R))
doc.close();doc=fitz.open(out)
for i in range(len(doc)):doc[i].get_pixmap(matrix=fitz.Matrix(1.35,1.35)).save('/tmp/016-qa-%s.png'%i)
