from pathlib import Path
from html import escape

OUT=Path(__file__).parent
HEAD='''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1800" height="1960" viewBox="0 0 1800 1960"><defs><marker id="arr" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto-start-reverse"><path d="M1 1 L8 5 L1 9" fill="none" stroke="#426d7d" stroke-width="1.7"/></marker></defs><rect width="1800" height="1960" fill="white"/><g font-family="PingFang SC,Noto Sans CJK SC,Microsoft YaHei,sans-serif">'''
p=[HEAD]
def t(x,y,s,size=24,color='#294959',weight=400,anchor='start'):
    p.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{anchor}">{escape(s)}</text>')
def box(x,y,w,h,title,sub=None,fill='#edf5f7',size=26):
    p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="13" fill="{fill}" stroke="#c6d8df" stroke-width="1.5"/>')
    t(x+w/2,y+(h/2+9 if sub is None else 37),title,size,weight=600,anchor='middle')
    if sub: t(x+w/2,y+73,sub,21,anchor='middle')
def arrow(x1,y1,x2,y2,both=False):
    p.append(f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="#426d7d" stroke-width="2" marker-end="url(#arr)" '+('marker-start="url(#arr)"' if both else '')+'/>')
def line(x1,y1,x2,y2):
    p.append(f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="#c6d8df" stroke-width="1.5"/>')
def section(y,n,q,kind):
    line(60,y-18,1740,y-18)
    t(60,y+28,n,34,'#147f88',600)
    t(190,y+28,q,33,'#173b4c',600)
    t(1740,y+28,kind,20,'#758892',anchor='end')
def cite(x,y,s,url):
    p.append(f'<a xlink:href="{escape(url,quote=True)}">');t(x,y,s,22,'#147f88',600);p.append('</a>')

t(60,64,'2.1 个人回忆与影像表达：三个问题的文献依据',39,'#173b4c',600)
t(60,110,'依文献内容重绘的概念示意｜箭头表达理论关系、使用过程或分析关系，不代表统一的因果模型。',22,'#758892')

section(160,'2.1.1','个人回忆是什么，又怎样形成？','理论研究')
cite(80,245,'[1] Conway & Pleydell-Pearce（2000）｜自我—记忆系统','https://pubmed.ncbi.nlm.nih.gov/10789197/')
box(90,285,320,92,'自传体知识','与自身经历有关的知识')
box(500,285,320,92,'当前目标','工作自我的关注与目的')
arrow(425,330,485,330,True)
line(250,377,250,402);line(660,377,660,402);line(250,402,660,402);arrow(455,402,455,425)
box(270,434,370,82,'线索引导的提取与建构',fill='#dceef0',size=25)
arrow(455,516,455,545)
t(455,579,'形成具体的自传体回忆',28,'#173b4c',600,'middle')

line(880,238,880,602)
cite(950,245,'[2] Rubin（2006）｜基本系统模型','https://pubmed.ncbi.nlm.nih.gov/26151796/')
box(990,288,240,62,'视觉与听觉',size=24)
box(1370,288,240,62,'空间与其他感官',size=24)
box(990,498,240,62,'语言与叙事',size=24)
box(1370,498,240,62,'情绪等系统',size=24)
box(1160,389,300,66,'情景记忆',fill='#dceef0',size=28)
arrow(1110,354,1194,384,True);arrow(1490,354,1427,384,True)
arrow(1110,494,1194,461,True);arrow(1490,494,1427,461,True)
t(1310,596,'多种系统相互作用；图中仅列部分系统',22,'#657c87',anchor='middle')
t(80,636,'理论要点：回忆具有建构性；回忆经验涉及多种系统，不能只按画面内容理解。',24,'#294959',600)

section(690,'2.1.2','照片和数字材料怎样参与回想？','方法研究＋过程观察')
cite(80,775,'[3] Harper（2002）｜照片引谈法','https://doi.org/10.1080/14725860220137345')
box(80,818,240,80,'照片进入访谈',size=25)
arrow(330,858,370,858)
box(380,818,240,80,'观看与讨论',size=25)
arrow(630,858,670,858)
box(680,818,230,80,'信息、感受与记忆',size=22)
t(80,943,'方法贡献：观察人如何借助影像讲述经历。',23)
t(80,980,'不能由此推定照片提高回忆准确性。',22,'#956f47')

line(940,768,940,1035)
cite(980,775,'[4] Hutmacher 等（2025）｜思维出声研究','https://doi.org/10.1186/s41235-025-00627-4')
t(980,815,'41 人：回忆约一年前的重要日与随机日',23)
box(980,850,270,80,'内部回忆',size=26)
box(1450,850,270,80,'外部资源',size=26)
arrow(1266,877,1434,877);arrow(1434,904,1266,904)
t(1350,955,'反复切换',22,'#147f88',600,'middle')
t(980,996,'随机日：数字资源使用量与内外切换次数更多。',22)
t(980,1031,'外部资源包括照片等，不限于影像。',21,'#657c87')
t(80,1080,'两类依据分别说明：影像可以参与讲述；回忆过程可以在内部经验与外部资料之间往返。',24,'#294959',600)

section(1135,'2.1.3','影像怎样组织经历并表达个人意义？','作品分析')
cite(80,1220,'[5] Rosas & Dittus（2021；在线发表于 2020）｜档案与蒙太奇','https://doi.org/10.1080/17503280.2020.1815123')
t(80,1260,'研究材料：Tarnation、51 Birch Street、The Marina Experiment 三部自传纪录片',23)
box(80,1310,310,100,'个人／家庭影像档案','既有影像材料',size=26)
arrow(402,1360,472,1360)
box(485,1310,350,100,'选择、蒙太奇与讲述','赋予材料新的语境',fill='#dceef0',size=26)
arrow(847,1360,917,1360)
box(930,1310,340,100,'自传影像叙事','组织过去与当下的理解',size=26)
arrow(1282,1360,1352,1360)
box(1365,1310,350,100,'自我与身份的表达','呈现、追问个人意义',size=26)
t(80,1460,'分析重点：个人影像被重新使用和组织，参与作者对自身及家庭关系的理解。',24,'#294959',600)
t(80,1502,'适用边界：这是叙事与自我呈现的研究，不能直接作为回忆能力改善的证据。',22,'#956f47')

line(60,1555,1740,1555)
t(60,1600,'文献出处',25,'#173b4c',600)
refs=[
 ('[1] Conway & Pleydell-Pearce. 2000. The construction of autobiographical memories in the self-memory system.', 'Psychological Review, 107(2), 261–288. DOI: 10.1037/0033-295X.107.2.261'),
 ('[2] Rubin. 2006. The Basic-Systems Model of Episodic Memory.', 'Perspectives on Psychological Science, 1(4), 277–311. DOI: 10.1111/j.1745-6916.2006.00017.x'),
 ('[3] Harper. 2002. Talking about pictures: A case for photo elicitation.', 'Visual Studies, 17(1), 13–26. DOI: 10.1080/14725860220137345'),
 ('[4] Hutmacher et al. 2025. Mediated autobiographical remembering in the digital age: insights from an experimental think-aloud study.', 'Cognitive Research: Principles and Implications, 10, 18. DOI: 10.1186/s41235-025-00627-4'),
 ('[5] Rosas & Dittus. 2021. The autobiographical documentary: archive and montage to represent the self.', 'Studies in Documentary Film, 15(3), 203–219. DOI: 10.1080/17503280.2020.1815123')]
for i,(a,b) in enumerate(refs):
    t(60,1640+i*57,a,18);t(60,1664+i*57,b,18,'#657c87')
t(60,1940,'重绘依据：论文摘要与现有章节核读记录；不是论文原图，也不表示本次完成了五篇文献的全文审计。',18,'#758892')
p.append('</g></svg>')
(OUT/'2.1-三个问题与文献依据.svg').write_text('\n'.join(p))
print(OUT/'2.1-三个问题与文献依据.svg')
