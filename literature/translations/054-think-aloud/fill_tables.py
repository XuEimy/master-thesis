"""Replace table labels while retaining original numerical cells and rules."""
from pathlib import Path
import fitz,json,html
ROOT=Path(__file__).resolve().parents[3];H=Path(__file__).parent
O=fitz.open(ROOT/'literature/sources/fulltext/E37-mediated-autobiographical-remembering-in.pdf');D=fitz.open(H/'054-原版式工作稿.pdf')
A=[p for p in (H/'中文译稿-进行中.md').read_text().split('\n\n') if p and not p.startswith('<!--')]
I=[]
def item(p,r,t,kind='label'):I.append(dict(page=p,rect=list(r),translation=t,kind=kind))
for p,b,ai in [(5,7,43),(7,4,53),(7,26,56),(8,5,62),(7,5,55),(7,27,58)]:item(p,O[p].get_text('blocks')[b][:4],A[ai].replace('**',''),'caption' if ai in [43,53,56,62] else 'note')
rows={5:{10:'从内部转向外部',11:'无内部记忆',12:'模糊的内部记忆',13:'详细的内部记忆',14:'从外部转向内部',15:'成功：确认',16:'成功：新增',17:'失败',18:'从外部转向外部',19:'切换总次数'},7:{7:'数字资源',8:'智能手机相册',9:'数字日历',10:'即时通讯',11:'Snapchat',12:'BeReal',13:'电子邮件',14:'互联网搜索',15:'数字笔记',16:'大学网站',17:'Instagram',18:'本地硬盘',19:'其他',20:'非数字资源',21:'印刷日历',22:'纸质日记',23:'社会资源',24:'家人',25:'伴侣',30:'数字资源',31:'非数字资源',32:'社会资源'},8:{9:'外部特征',10:'地点',11:'事件',12:'人物',13:'交谈内容',14:'内部状态',15:'想法',16:'感受',17:'总计'}}
for p,m in rows.items():
 bs=O[p].get_text('dict')['blocks']
 for b,t in m.items():
  spans=[s for l in bs[b]['lines'] for s in l['spans'] if s['bbox'][0]<(420 if p==5 else (134 if p==8 else 150))]
  r=fitz.Rect(spans[0]['bbox'])
  for s in spans[1:]:r|=fitz.Rect(s['bbox'])
  item(p,r,t)
for p,bs in [(5,[8]),(7,[6,28]),(8,[6,7])]:
 for b in bs:
  for l in O[p].get_text('dict')['blocks'][b]['lines']:
   for s in l['spans']:
    t={'important day':'重要日期','random day':'随机日期','internal retrieval':'内部提取','external retrieval':'外部提取'}[s['text'].lower()];item(p,s['bbox'],t)
for x in I:D[x['page']].add_redact_annot(fitz.Rect(x['rect']),fill=(1,1,1))
for p in D:p.apply_redactions(images=0,graphics=0)
for x in I:
 p=D[x['page']];r=fitz.Rect(x['rect'])
 if x['kind']=='label':
  size=7.2;r.x1=max(r.x1,r.x0+len(x['translation'])*size+2);r.y1=r.y0+12
 else:
  r.x1=540.9 if r.x0>300 or x['page']==8 else 292.9;r.y1+=1
  size=8 if x['kind']=='caption' else 6.8
 css=f"@font-face{{font-family:cn;src:url('songti.ttf')}}body{{margin:0;font-family:cn;font-size:{size}pt;line-height:1.05}}"
 spare,scale=p.insert_htmlbox(r,'<p style="margin:0">'+html.escape(x['translation'])+'</p>',css=css,archive=fitz.Archive(str(ROOT/'tmp/pdfs')),scale_low=.8)
 assert spare>=0,(x,spare);x['font_size']=size*scale
D.save(H/'054-原版式校对稿.pdf',garbage=4,deflate=True)
(H/'表格文字映射.json').write_text(json.dumps(I,ensure_ascii=False,indent=2))
print('table labels/captions',len(I),'pages',len(D))
for i in [5,7,8]:D[i].get_pixmap(matrix=fitz.Matrix(1.4,1.4)).save(ROOT/f'tmp/pdfs/054-table-page{i+1}.png')
