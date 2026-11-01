"""053 原版式排版工作稿；逐块映射在此明确列出，表格和图内文字另行处理。"""
import json,re,html
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).parent
row=next(x for x in json.loads((ROOT/'literature/translations/全量精读翻译队列.json').read_text()) if x['number']==53)
doc=fitz.open(ROOT/row['source']);blocks={i:p.get_text('blocks') for i,p in enumerate(doc)}
md=(HERE/'中文译稿-进行中.md').read_text();sections={};title=''
for b in md.split('\n\n'):
 if b.startswith('#'):title=re.sub(r'^#+ ','',b);sections[title]=[]
 elif b.strip():sections.setdefault(title,[]).append(b.strip())
# PDF zero-based page and block indices, in semantic paragraph order.
body={
'1. 引言': [[(1,8)],[(1,9),(1,10)],[(1,11)],[(2,0)],[(2,1)],[(2,2)],[(2,3)],[(2,4),(2,5)],[(2,6)],[(2,7)],[(2,8),(3,0)],[(3,1)]],
'2.1. 参与者':[[(3,4)]],'2.2. 设计':[[(3,6),(3,7)]],
'3. 材料与流程':[[(3,9)]],
'3.1.1. 第一天':[[(3,12)],[(3,13)],[(3,14)],[(3,15)],[(3,16)]],
'3.1.2. 第二天':[[(3,18),(4,0)]],
'3.1.3. 第三天':[[(4,2)],[(4,3)],[(4,4)]],
'3.2. 平衡程序':[[(4,6)]],'3.3. 数据分析':[[(4,8),(5,0)],[(5,1)]],
'5. 主观情景记忆':[[(6,1)],[(6,2)]],
'6. 客观情景记忆':[[(6,4),(6,5)],[(6,6),(6,7)]],
'7. 讨论':[[(6,9)],[(6,10),(7,0)],[(7,1)],[(7,2),(7,3)],[(7,4)]],
'8. 优势与局限':[[(7,6),(8,0)]],'9. 结论':[[(8,2),(8,3)]]}
heads={'1. 引言':(1,7),'2. 方法':(3,2),'2.1. 参与者':(3,3),'2.2. 设计':(3,5),'3. 材料与流程':(3,8),'3.1. 流程':(3,10),'3.1.1. 第一天':(3,11),'3.1.2. 第二天':(3,17),'3.1.3. 第三天':(4,1),'3.2. 平衡程序':(4,5),'3.3. 数据分析':(4,7),'4. 结果':(5,2),'5. 主观情景记忆':(6,0),'6. 客观情景记忆':(6,3),'7. 讨论':(6,8),'8. 优势与局限':(7,5),'9. 结论':(8,1),'CRediT 作者贡献声明':(8,4),'利益冲突声明':(8,6),'数据可用性':(9,37)}
items=[]
def add(p,b,t,kind='body'):
 r=list(blocks[p][b][:4]);items.append({'page':p,'block':b,'source_rect':r,'text':t,'kind':kind,'source':blocks[p][b][4]})
for sec,groups in body.items():
 pars=sections[sec];assert len(groups)==len(pars),(sec,len(groups),len(pars))
 for refs,t in zip(groups,pars):
  if len(refs)==1:add(*refs[0],t);continue
  weights=[len(blocks[p][b][4]) for p,b in refs];pos=0
  for j,(p,b) in enumerate(refs):
   if j==len(refs)-1:cut=len(t)
   else:
    target=int(len(t)*sum(weights[:j+1])/sum(weights));choices=[i+1 for i,c in enumerate(t) if i>=pos and c in '。；，' and abs(i-target)<90]
    cut=min(choices,key=lambda k:abs(k-target)) if choices else target
   add(p,b,t[pos:cut]);pos=cut
for t,(p,b) in heads.items():add(p,b,t,'heading')
add(1,0,'第一人称与第三人称生活日志改善情景记忆','title')
add(1,2,'a 荷兰乌得勒支大学赫尔姆霍兹研究所实验心理学部门。\nb 荷兰鹿特丹 Slingedael 科萨科夫综合征专业中心，Slinge 901，3086 EZ。','small')
add(1,3,'文章信息','heading');add(1,4,'关键词：\n生活日志记录\n遗忘症\n记忆巩固\n记忆提取\n辅助技术\nSenseCam\n神经心理康复','small');add(1,5,'摘要','heading');add(1,6,sections['摘要'][0])
add(8,5,'\n'.join(sections['CRediT 作者贡献声明']),'small');add(8,7,sections['利益冲突声明'][0]);add(9,38,sections['数据可用性'][0])
for (p,b),t in zip([(4,9),(4,10),(5,21),(5,22)],sections['图注译文（排版时回填原位）']):add(p,b,t.replace('**',''),'small')
for x in items:doc[x['page']].add_redact_annot(fitz.Rect(x['source_rect']),fill=(1,1,1))
for p in doc:p.apply_redactions(images=0,graphics=0)
font=ROOT/'tmp/pdfs/songti.ttf';assert font.exists(),'Prepare a suitable regular Chinese font first'
for x in items:
 r=fitz.Rect(x['source_rect']);r.y1+=1
 if x['kind'] in ['heading','title']:r.x1=560 if r.x0>300 or x['kind']=='title' else 291
 size={'body':9,'heading':9,'title':14,'small':7.5}[x['kind']]
 css=f"@font-face{{font-family:cn;src:url('{font.name}')}} body{{margin:0}} p{{margin:0;font-family:cn;font-size:{size}pt;line-height:1.18;overflow-wrap:anywhere}}"
 text=html.escape(x['text']).replace('\n','<br>');spare,scale=doc[x['page']].insert_htmlbox(r,'<p>'+text+'</p>',css=css,archive=fitz.Archive(str(font.parent)),scale_low=.8)
 if spare<0:raise ValueError(('overflow',x['page'],x['block']))
 x['used_font_size']=size*scale
for p in doc:p.insert_text((38,775),'WORK IN PROGRESS - tables and figure labels pending',fontsize=7,color=(.7,0,0))
doc.save(HERE/'053-原版式排版工作稿.pdf',garbage=4,deflate=True)
(HERE/'版面映射-进行中.json').write_text(json.dumps(items,ensure_ascii=False,indent=2))
print('Draft only:',len(doc),'pages',len(items),'translated regions; tables and figure labels pending')
