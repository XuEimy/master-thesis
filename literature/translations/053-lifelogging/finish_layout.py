import fitz,json,re,html
from pathlib import Path
HERE=Path(__file__).parent;ROOT=HERE.parents[2]
pdf=fitz.open(HERE/'053-原版式排版工作稿.pdf');md=(HERE/'中文译稿-进行中.md').read_text();font=ROOT/'tmp/pdfs/songti.ttf';archive=fitz.Archive(str(font.parent))
css="@font-face{font-family:cn;src:url('songti.ttf')}body{margin:0;font-family:cn}p{margin:0;font-size:8pt;line-height:1.15} table{border-collapse:collapse;width:100%;font-size:7.2pt;line-height:1.12}td,th{padding:2px 3px;border-bottom:0.3px solid #aaa;vertical-align:top;text-align:left}th{font-weight:bold;border-top:0.6px solid black}"
items=[]
def box(page,rect,text=None,markup=None,size=8):
 items.append(dict(page=page,rect=rect,text=text,markup=markup,size=size))
def table(n):
 s=re.split(r'\n#{2,3} ',md.split('### 表'+str(n))[1],maxsplit=1)[0];lines=s.splitlines();rows=[]
 for l in lines:
  if l.startswith('|') and not re.match(r'^\|[-:| ]+\|$',l):rows.append([x.strip() for x in l.strip('|').split('|')])
 return rows

def thtml(rows):return '<table>'+''.join('<tr>'+''.join(('<th>' if i==0 else '<td>')+html.escape(c)+('</th>' if i==0 else '</td>') for c in row)+'</tr>' for i,row in enumerate(rows))+'</table>'
# Table regions retain original placement. Original footnotes are included explicitly.
box(5,[306,490,561,716],markup='<p>表1　两视角组的均值M（标准差SD），各n=16。</p>'+thtml(table(1))+'<p>第一人称＝自我中心；第三人称＝非自我中心。得分范围按原文保留。</p>')
box(6,[37,52,561,176],markup='<p>表2　各支持类型下自我报告的记忆提取视角频数（各组n=16）。</p>'+thtml(table(2))+'<p>注：频数为各条件下报告采用自我中心、非自我中心或两种视角提取事件记忆的人数。</p>')
box(8,[37,264,561,283],text='附录 A. 主观情景记忆强度测验',size=9)
options='Q11选项：第一人称（从自己的眼睛所见）；第三人称（从另一观察点）；两种视角；没有特定视角；不理解问题。'
box(8,[37,303,561,594],markup='<p>表3　主观情景记忆强度及提取视角题项。Q1–Q10均采用“非常不同意”到“非常同意”的七点量表。</p>'+thtml(table(3))+'<p>'+options+'</p>')
box(8,[37,616,561,634],text='附录 B. 客观情景记忆强度测验',size=9)
t4=table(4)
box(8,[37,655,561,744],markup='<p>表4　客观情景记忆强度题项与评分。a：视觉信息；b：非视觉信息。</p>'+thtml(t4[:2])+'<p>（续下页）</p>')
box(9,[37,50,561,506],markup='<p>表4（续）</p>'+thtml([t4[0]]+t4[2:])+'<p>a：视觉信息题项。b：非视觉信息题项。</p>')
box(9,[37,513,561,532],text='附录 C. 实验结束问卷',size=9)
box(9,[37,552,561,631],markup='<p>表5　实验结束问卷</p>'+thtml(table(5)))
# Remaining front matter metadata; original title and DOI stay searchable.
box(1,[42,669,560,679],text='* 通讯作者：荷兰乌得勒支大学赫尔姆霍兹研究所实验心理学部门。',size=7)
box(1,[49,679,560,691],text='电子邮件：e.oudman@leliezorggroep.nl（E. Oudman）。',size=7)
box(1,[37,696,560,714],text='https://doi.org/10.1016/j.actpsy.2025.104929\n收稿：2024-07-02；修订稿：2025-02-10；接收：2025-03-17。',size=7)
box(1,[37,715,561,737],text='在线发表：2025-03-19。© 2025 原作者。Elsevier B.V. 出版。本文采用 CC BY 4.0 开放许可（http://creativecommons.org/licenses/by/4.0/）。',size=7)
box(9,[37,706,291,720],text='参考文献',size=9)
# Remove draft footer and replace translation targets; white covers also remove old table rules.
for p in pdf:
 for r in p.search_for('WORK IN PROGRESS - tables and figure labels pending'):p.add_redact_annot(r,fill=(1,1,1))
for it in items:pdf[it['page']].add_redact_annot(fitz.Rect(it['rect']),fill=(1,1,1))
for p in pdf:p.apply_redactions(images=0,graphics=0)
for it in items:
 p=pdf[it['page']];r=fitz.Rect(it['rect']);p.draw_rect(r,fill=(1,1,1),color=None)
 content=it['markup'] or '<p style="font-size:'+str(it['size'])+'pt">'+html.escape(it['text']).replace('\n','<br>')+'</p>'
 spare,scale=p.insert_htmlbox(r,content,css=css,archive=archive,scale_low=.72)
 if spare<0:raise ValueError(('overflow',it['page'],it['rect']))
 it['scale']=scale
# Figure 1 is raster; preserve all geometry and cover label interiors only.
fig=json.loads((HERE/'图1文字映射.json').read_text())
for item in fig['labels']:
 r=fitz.Rect(item['rect']);p=pdf[4];p.draw_rect(r,color=None,fill=(1,1,1))
 spare,scale=p.insert_htmlbox(r,'<p style="text-align:center;font-size:7pt">'+html.escape(item['translation']).replace('\n','<br>')+'</p>',css=css,archive=archive,scale_low=.7)
 if spare<0:raise ValueError(('figure overflow',item))
# Provenance on institutional cover, in its blank lower half.
boxtext='中文译本｜原作：Oudman、Klukas、van Teijlingen、Postma（2025）\n原作许可：CC BY 4.0。AI中文翻译，2026-10-31，未经作者审定。\n保留原刊页面、双栏、图表位置和页码；中文换行与表格行列作适配。\n参考文献题录保留英文。原文评分范围、题项重复及措辞疑点见随附核对说明。'
pdf[0].insert_htmlbox(fitz.Rect(45,510,550,670),'<p style="font-size:10pt">'+html.escape(boxtext).replace('\n','<br>')+'</p>',css=css,archive=archive)
pdf.set_metadata({'title':'第一人称与第三人称生活日志改善情景记忆｜中文原版式译本','author':'Erik Oudman; Isabelle F. Klukas; Tijmen van Teijlingen; Albert Postma','subject':'CC BY 4.0; AI中文翻译，2026-10-31，未经作者审定'})
out=ROOT/'output/pdf/053-第一人称与第三人称生活日志-中文原版式译本.pdf';pdf.save(out,garbage=4,deflate=True)
(HERE/'表格排版核对.json').write_text(json.dumps(items,ensure_ascii=False,indent=2))
print(out, 'minimum table scale',min(i.get('scale',1) for i in items))
for i,p in enumerate(pdf):p.get_pixmap(matrix=fitz.Matrix(1.4,1.4)).save(ROOT/f'tmp/pdfs/053-final-{i+1}.png')
