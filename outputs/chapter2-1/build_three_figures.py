from pathlib import Path
from html import escape

OUT=Path(__file__).parent
W,H=1600,900
INK='#163f51'; BLUE='#176a83'; TEAL='#138b91'; MUTED='#607e8b'

class Figure:
    def __init__(self,section,title,claim):
        self.p=['''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1600" height="900" viewBox="0 0 1600 900"><defs><marker id="a" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto-start-reverse"><path d="M1 1 L8 5 L1 9" fill="none" stroke="#176a83" stroke-width="1.7"/></marker></defs><rect width="1600" height="900" fill="#f6fbfd"/><g font-family="PingFang SC,Noto Sans CJK SC,Microsoft YaHei,sans-serif">''']
        self.text(70,54,section,22,TEAL,600)
        self.text(70,117,title,39,INK,600)
        self.text(70,165,claim,26,BLUE)
        self.path('M70 195 H1530',color='#c9dee5',arrow=False)
    def text(self,x,y,s,size=26,color=INK,bold=400,anchor='start'):
        self.p.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{bold}" text-anchor="{anchor}">{escape(s)}</text>')
    def lines(self,x,y,lines,size=24,color=INK,bold=400,anchor='start',gap=36):
        for i,s in enumerate(lines): self.text(x,y+i*gap,s,size,color,bold,anchor)
    def rect(self,x,y,w,h,fill='#fff',stroke='#b7d2dc',r=16,dash=False):
        self.p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="2" '+('stroke-dasharray="7 7"' if dash else '')+'/>')
    def path(self,d,color=BLUE,arrow=True,both=False):
        self.p.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2.5" '+('marker-end="url(#a)"' if arrow else '')+(' marker-start="url(#a)"' if both else '')+'/>')
    def node(self,x,y,w,h,title,sub=None,fill='#e6f4f6'):
        self.rect(x,y,w,h,fill)
        self.text(x+w/2,y+(h/2+10 if not sub else 49),title,29,INK,600,'middle')
        if sub:self.text(x+w/2,y+88,sub,22,MUTED,400,'middle')
    def cite(self,x,y,s,url):
        self.p.append(f'<a xlink:href="{escape(url,quote=True)}">');self.text(x,y,s,21,BLUE);self.p.append('</a>')
    def footer(self,s):
        self.path('M70 794 H1530',color='#c9dee5',arrow=False)
        self.text(70,868,s,19,MUTED)
    def save(self,name):
        (OUT/(name+'.svg')).write_text('\n'.join(self.p+['</g></svg>']))

f=Figure('2.1.1  个人回忆','个人回忆怎样形成？','既有自传体知识与当前目标共同参与具体回忆的建构。')
f.rect(105,250,1430,355,'#fff','#a8ccd6',22,True)
f.text(135,290,'自我—记忆系统（简化示意）',23,TEAL,600)
f.node(145,325,315,100,'自传体知识',fill='#e6f4f6')
f.node(145,485,315,90,'当前目标',fill='#e6f4f6')
f.path('M285 439 V471')
f.path('M315 471 V439')
f.text(328,461,'相互联系',19,MUTED)
f.node(620,375,390,135,'线索引导的提取与建构','提取、组织与自身有关的信息',fill='#d4edf0')
f.path('M460 375 H535 V420 H605')
f.path('M460 530 H535 V469 H605')
f.path('M1010 443 H1170')
f.text(1100,417,'形成',21,BLUE,anchor='middle')
f.node(1185,375,310,135,'具体的个人回忆','亲历事件及其体验',fill='#d4edf0')
f.text(105,654,'补充视角 · 基本系统模型',23,TEAL,600)
f.text(105,690,'视觉、听觉、空间、语言、情绪与叙事等系统相互作用，共同参与情景记忆。',25)
f.text(105,737,'这一模型补充说明回忆经验的多种成分，不与上图合并为同一套理论。',21,MUTED)
f.footer('依据文献内容重绘；图示省略理论细节，不是论文原图。')
f.cite(70,827,'主图：Conway & Pleydell-Pearce, 2000 · Psychological Review','https://pubmed.ncbi.nlm.nih.gov/10789197/')
f.cite(910,827,'补充：Rubin, 2006 · Perspectives on Psychological Science','https://pubmed.ncbi.nlm.nih.gov/26151796/')
f.save('2.1.1-个人回忆怎样形成')

f=Figure('2.1.2  影像与回忆','影像怎样参与回想？','回忆过程可以在内部经验与外部资料之间反复往返。')
f.rect(105,255,490,320,'#fff','#b7d2dc',26)
f.rect(1005,255,490,320,'#fff','#b7d2dc',26)
f.text(350,315,'内部回忆',34,INK,600,'middle')
f.lines(350,375,['自己想起的人物、行动、对话','以及当时的想法和感受'],25,anchor='middle',gap=45)
f.text(350,530,'想起了什么？还有什么不清楚？',22,MUTED,anchor='middle')
f.text(1250,315,'外部资料',34,INK,600,'middle')
for x,y,w,s in [(1040,348,180,'照片／视频'),(1250,348,205,'聊天记录'),(1040,425,180,'日记'),(1250,425,205,'其他资料')]:
    f.rect(x,y,w,58,'#e6f4f6',r=10);f.text(x+w/2,y+38,s,25,anchor='middle')
f.text(1250,530,'影像是外部资料的一部分',22,MUTED,anchor='middle')
f.path('M615 363 H985')
f.text(800,335,'查找、查看资料',24,BLUE,600,'middle')
f.path('M985 470 H615')
f.text(800,511,'结合资料继续回想',24,BLUE,600,'middle')
f.text(800,427,'反复往返',23,TEAL,600,'middle')
f.text(105,623,'研究观察',23,TEAL,600)
f.text(270,623,'41 人回忆约一年前的重要日与随机日；随机日使用更多数字资源、发生更多切换。',24)
f.text(105,683,'方法依据',23,TEAL,600)
f.text(270,683,'照片引谈：将照片带入访谈，通过观看与讨论引出信息、感受和记忆。',24)
f.text(270,737,'需要区分：从材料中得知信息，与本人重新想起经历。',22,MUTED)
f.footer('往返关系为研究过程的概括；引出讲述或增加资料使用，不等于提高回忆准确性。')
f.cite(70,827,'过程：Hutmacher et al., 2025 · Cognitive Research: Principles and Implications','https://doi.org/10.1186/s41235-025-00627-4')
f.cite(1100,827,'方法：Harper, 2002 · Visual Studies','https://doi.org/10.1080/14725860220137345')
f.save('2.1.2-影像怎样参与回想')

f=Figure('2.1.3  影像表达','影像怎样表达个人经历？','个人影像经重新组织和讲述，参与自传叙事与自我表达。')
# Archive stack, an actual material-to-expression relationship rather than equal text columns.
f.rect(145,310,300,230,'#eff5f8',r=10)
f.rect(125,330,300,230,'#e6f4f6',r=10)
f.rect(105,350,300,230,'#fff',r=10)
f.text(255,410,'个人／家庭',29,INK,600,'middle')
f.text(255,453,'影像档案',32,INK,600,'middle')
f.text(255,520,'既有照片与活动影像',23,MUTED,anchor='middle')
f.path('M430 452 H565')
f.text(502,422,'重新使用',21,BLUE,anchor='middle')
f.rect(585,300,430,300,'#d4edf0','#a8ccd6',22)
f.text(800,352,'重新语境化',32,INK,600,'middle')
for y,s in [(378,'选择哪些材料'),(443,'怎样剪辑与排列'),(508,'怎样结合作者讲述')]:
    f.rect(630,y,340,51,'#fff','#bad5dc',10)
    f.text(800,y+34,s,25,anchor='middle')
f.path('M1030 452 H1100 V377 H1160')
f.text(1070,487,'组织为',21,BLUE,anchor='middle')
f.node(1180,320,330,115,'自传影像叙事','讲述过去与当下的理解',fill='#e6f4f6')
f.path('M1345 449 V484')
f.node(1180,500,330,100,'自我与关系的表达',fill='#d4edf0')
f.text(105,660,'作品分析',23,TEAL,600)
f.text(270,660,'Tarnation · 51 Birch Street · The Marina Experiment',26)
f.text(105,713,'三部作品用于分析：个人影像如何通过新的叙事语境参与身份与自我的表达。',25)
f.footer('研究对象是影像叙事与自我呈现；这条表达关系不作为回忆能力改善的证据。')
f.cite(70,827,'Rosas & Dittus, 2021（在线发表于 2020）· Studies in Documentary Film','https://doi.org/10.1080/17503280.2020.1815123')
f.text(1530,827,'据作品分析重绘',21,MUTED,anchor='end')
f.save('2.1.3-影像怎样表达个人经历')
print('Generated three editable SVG figures.')
