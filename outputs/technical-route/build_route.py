from pathlib import Path
from html import escape

OUT = Path(__file__).parent
parts = ['''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="2100" viewBox="0 0 1600 2100">
<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,1 L8,5 L0,9" fill="none" stroke="#456377" stroke-width="1.5"/></marker><marker id="back" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,1 L8,5 L0,9" fill="none" stroke="#b87539" stroke-width="1.5"/></marker></defs>
<rect width="1600" height="2100" fill="#ffffff"/>
<g font-family="PingFang SC,Noto Sans CJK SC,Microsoft YaHei,sans-serif">''']

def rect(x,y,w,h,fill='#f3f7fa',stroke='#cbd7df',rx=12):
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')

def text(x,y,lines,size=23,color='#344d60',weight=400,step=34):
    if isinstance(lines,str): lines=[lines]
    for i,line in enumerate(lines):
        parts.append(f'<text x="{x}" y="{y+i*step}" font-size="{size}" fill="{color}" font-weight="{weight}">{escape(line)}</text>')

def path(d,back=False):
    color='#b87539' if back else '#456377'
    dash='stroke-dasharray="8 7"' if back else ''
    parts.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2" {dash} marker-end="url(#{"back" if back else "arrow"})"/>')

text(60,65,'个人回忆唤起研究 · 技术路线',40,'#183549',600)
text(60,110,'研究聚焦：个人线索如何转化为记录内容，并参与 AI 材料组织与影像表达',25)
text(60,153,'拟议研究方案｜实线：研究推进　虚线：依据失败环节返回修订',20,'#657783')
text(60,206,'研究任务',22,'#657783',600)
text(250,206,'研究步骤与关键关系',22,'#657783',600)
text(1140,206,'研究方法与阶段产出',22,'#657783',600)

# Ten steps, grouped into the four current research tasks.
steps=[
 (240,110,'01  确定情境与对象',['具体亲历事件、已有材料、记录习惯与回看经历']),
 (378,165,'02  分析线索与使用条件',None),
 (571,125,'03  建立初步关联框架',['个人线索 → 记录内容 → 组织与表达方式','登记适用情境、证据来源、使用代价与反例']),
 (735,165,'04  联合探索记录与交互方案',None),
 (928,110,'05  采集试用与筛选',['检查目标线索保留、信息遗漏、操作负担与活动打断']),
 (1066,110,'06  整理可追溯材料',['原始记录＋本人补述＋时间与情境信息＋处理记录']),
 (1215,165,'07  开发 AI 辅助与回看交互',None),
 (1408,125,'08  整合原型与先导测试',['采集 → 关联 → 线索确认 → AI 组织与表达 → 回看修改','检查可运行性、任务理解、条件差异；确定测量与研究规模']),
 (1572,225,'09  比较材料选择与组织依据',['候选条件：A 原始材料回看；B AI 按时间／事件组织','主要对照：B ↔ C；C 为 AI 结合本人确认的关键线索组织','核心结果：回忆是否发生、事件与体验内容、表达贴切度','另行评价：来源辨认、可核对事实一致性、使用负担','控制／记录：素材池、输出时长、前期接触、用户投入与顺序']),
 (1825,125,'10  综合结果，验证并修订框架',['得到支持／部分条件支持／暂未支持／证据不足','形成有适用边界的关联框架、设计原则与原型'])
]
for i,(y,h,title,lines) in enumerate(steps):
    rect(250,y,830,h)
    text(276,y+37,title,27,'#183549',600)
    if lines: text(276,y+77,lines,22,step=31)
    if i<len(steps)-1:
        path(f'M665,{y+h} L665,{steps[i+1][0]-5}')

def pair(y,left,right):
    parts.append(f'<path d="M665,{y+60} V{y+146}" stroke="#cbd7df"/>')
    text(276,y+82,left[0],23,'#116777',600)
    text(276,y+115,left[1:],21,step=28)
    text(687,y+82,right[0],23,'#116777',600)
    text(687,y+115,right[1:],21,step=28)

pair(378,['回忆线索与记录需要','材料与讲述对照、信息缺口','区分回忆、复述与推断'],['记录行为与使用条件','记录时机、操作与携带','可接受负担及用户控制'])
pair(735,['记录策略、输入与硬件','按线索需要联合选择','采集能力与个人习惯共同约束'],['本人参与与交互方式','确认线索、补述与修改','检查框架能否解释设计取舍'])
pair(1215,['07A  AI 辅助处理','筛选、检索、事件关联与组织','保留来源，检查遗漏与错误关联'],['07B  回看与表达交互','本人确认、选择、补述与修改','区分表达意图和事实依据'])

groups=[
 (240,456,'任务一',['建立','关联框架'],'RQ1', ['方法','文献综合、个人材料引谈','情境观察、跨案例分析','','产出','线索与记录需求','有证据的初步关联框架']),
 (735,441,'任务二',['设计试用','调整框架'],'RQ2 → RQ3',['方法','记录探针、方案比较','采集与交互试用','','产出','记录和交互策略','输入与硬件方案','可追溯材料集']),
 (1215,318,'任务三',['实现','整合原型'],'RQ3',['方法','软硬件集成、错误分析','先导测试','','产出','可运行的整合原型','主要比较与测量方案']),
 (1572,378,'任务四',['验证','完善框架'],'回应 RQ1—3',['方法','比较研究、内容编码','访谈与适当统计分析','','产出','作用证据与失败案例','修订框架及适用边界'])
]
for y,h,label,lines,rq,details in groups:
    rect(45,y,145,h,'#eaf2f5','#eaf2f5')
    text(62,y+42,label,24,'#116777',600)
    text(62,y+92,lines,25,'#183549',600,38)
    text(57,y+h-27,rq,16,'#657783')
    rect(1130,y,425,h,'#f8fafb','#dce3e7')
    text(1153,y+42,details,22,step=35)
    path(f'M1080,{y+h-38} H1125')

# Feedback rails sit outside the process nodes and do not cross text.
path('M250,1887 H216 V460 H245',True)
path('M216,817 H245',True)
path('M216,1297 H245',True)
path('M1080,983 H1105 V818 H1085',True)
text(60,2000,'反馈修订：线索解释不足 → 02／03；采集不足或负担过高 → 04／05；组织或表达问题 → 07A／07B',21,'#925d2e')
text(60,2037,'主要比较聚焦组织依据；具体条件经先导确定。回忆、表达与事实一致性分别判断。',21,'#657783')
text(60,2074,'依据：第二章研究缺口与第三章研究方案 · 2026-10-28',18,'#657783')
parts.append('</g></svg>')
(OUT/'技术路线.svg').write_text('\n'.join(parts))
print(OUT/'技术路线.svg')
