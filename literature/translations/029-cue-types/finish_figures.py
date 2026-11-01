from pathlib import Path
import fitz,html,json
ROOT=Path(__file__).resolve().parents[3];D=Path(__file__).parent
src=fitz.open(next((ROOT/'literature/sources/fulltext').glob('029-*.pdf')))
doc=fitz.open(ROOT/'output/pdf/029-线索类型与自传体记忆-表格排版草稿.pdf')
R=[]
# Pixel rectangles refer to inspected 2x page clips; underlying raster figures stay intact.
def lab(p,im,box,text,size=8,bg=(1,1,1),rotate=0):
 origin=src[p].get_image_info()[im]['bbox']; x,y=origin[:2]
 rect=[x+box[0]/2,y+box[1]/2,x+box[2]/2,y+box[3]/2]
 R.append(dict(page=p,rect=rect,text=text,size=size,bg=bg,rotate=rotate))
def legend(p,im,positions):
 for box,t in zip(positions,['年龄组','老年人','年轻人']):lab(p,im,box,t,7)
def row(p,im,centers,y,labels,width=65):
 for x,t in zip(centers,labels):lab(p,im,[x-width/2,y,x+width/2,y+22],t,7.5)
gray=(.95,.95,.95)
legend(6,0,[[387,0,424,22],[455,0,496,22],[528,0,575,22]])
for box,t in [([210,48,320,70],'全部反应'),([645,48,750,70],'情景性记忆')]:lab(6,0,box,t,7.5,gray)
row(6,0,[101,183,265,345,427,533,614,695,777,858],506,['句子','词语','问题','照片','视频']*2)
lab(6,0,[430,528,535,546],'线索形式',7.5);lab(6,0,[0,232,19,340],'提取率',8,rotate=90)
legend(7,0,[[394,0,433,22],[464,0,503,22],[537,0,582,22]])
for y in [48,585]:
 for x,t in [(230,'评价线索'),(670,'事件线索')]:lab(7,0,[x,y,x+88,y+22],t,7.5,gray)
for y in [514,1051]:row(7,0,[134,269,403,572,706,840],y,['句子','词语','问题','词语','问题','照片'])
for y in [235,773]:lab(7,0,[0,y,20,y+110],'提取率',8,rotate=90)
lab(7,0,[441,1074,545,1091],'线索形式',7.5)
legend(8,0,[[367,0,405,22],[432,0,474,22],[503,0,546,22]])
for x,y,t in [(145,46,'句子'),(430,46,'词语'),(701,46,'问题'),(145,279,'照片'),(430,279,'视频')]:lab(8,0,[x,y,x+72,y+20],t,7.5,gray)
row(8,0,[122,242,361,424,487,550,667,787],248,['评价','意象','评价','事件','地点','社会','评价','事件'],60)
row(8,0,[100,182,265],482,['事件','地点','物件'])
row(8,0,[396,515],482,['事件／地点','物件／意象'],115)
lab(8,0,[0,213,20,325],'提取率',8,rotate=90);lab(8,0,[410,503,505,519],'线索形式',7.5)
legend(8,1,[[372,0,408,22],[438,0,478,22],[506,0,551,22]])
for box,t in [([197,46,315,67],'编码年龄'),([622,46,715,67],'重要性'),([216,279,300,300],'复述'),([625,279,713,300],'生动性')]:lab(8,1,box,t,7.5,gray)
for y in [248,481]:row(8,1,[113,209,304,399,522,617,712,807],y,['词语','问题','照片','视频']*2)
lab(8,1,[0,242,20,303],'z分数',8,rotate=90);lab(8,1,[400,505,503,522],'线索形式',7.5)
# Draw only over inspected text labels, avoiding ticks, lines and data.
for pg,im,boxes in [(6,0,[[54,507,908,529]]),(7,0,[[55,514,923,536],[55,1051,923,1074]]),(8,0,[[51,248,860,271],[51,482,589,504]]),(8,1,[[55,248,866,272],[55,481,866,504]])]:
 origin=src[pg].get_image_info()[im]["bbox"]
 for b in boxes:
  rr=fitz.Rect(origin[0]+b[0]/2,origin[1]+b[1]/2,origin[0]+b[2]/2,origin[1]+b[3]/2)
  doc[pg].draw_rect(rr,color=None,fill=(1,1,1),overlay=True)
for r in R:doc[r['page']].draw_rect(fitz.Rect(r['rect']),color=None,fill=r['bg'],overlay=True)
# Original text metadata replacements.
M=[([44,612.3,507,624.2],'* 通讯地址：英国利兹大学心理学院，Woodhouse Lane，Leeds LS2 9JT。',7),([51,622.1,507,635],'电子邮箱：a.mair@leeds.ac.uk',7),([39,653.4,507,663.9],'收稿：2025年9月12日；修订稿：2025年11月26日；接受：2025年12月22日。',7),([38.8,664,508,692],'在线发表：2025年12月24日。1053-8100／© 2025 作者。Elsevier Inc.出版。本文依CC BY 4.0许可开放获取：https://creativecommons.org/licenses/by/4.0/',7)]
for rect,t,size in M:doc[0].add_redact_annot(fitz.Rect(rect),fill=False)
doc[0].apply_redactions(images=0,graphics=0)
for rect,t,size in M:R.append(dict(page=0,rect=rect,text=t,size=size,rotate=0))
R.append(dict(page=15,rect=[39,575,507,685],size=8,rotate=0,text='译本说明：原作 Ali Mair，Consciousness and Cognition 138 (2026), 103983；DOI：10.1016/j.concog.2025.103983。依 CC BY 4.0 许可翻译，AI译文未经作者审定，参考文献保留原文。\n核对提示：图1原图为左右面板，原图注“下方面板”应指右侧。年轻组总人数51，原文性别人数34与7合计41；正文与表1的两项标准差略有差异；研究2概述与详细排除原因表述不同。表6原注阈值写r > 0.10，但表内也列负向关联。译文保留这些原始表述，详细核对说明随译稿保存。'))
for r in R:
 css="@font-face{font-family:cn;src:url('songti.ttf')}body{font-family:cn;font-size:%spt;margin:0;padding:0;line-height:1.1}"%r['size']
 spare,scale=doc[r['page']].insert_htmlbox(fitz.Rect(r['rect']),html.escape(r['text']).replace('\n','<br>'),css=css,archive=fitz.Archive(str(ROOT/'tmp/pdfs')),rotate=r['rotate'],scale_low=.8)
 r.update(spare=spare,scale=scale)
 if spare<0:raise RuntimeError(r)
out=ROOT/'output/pdf/029-线索类型与自传体记忆-中文待验收.pdf';doc.save(out,garbage=4,deflate=True)
(D/'图中文字与出版信息映射.json').write_text(json.dumps(R,ensure_ascii=False,indent=2))
print(out);print('regions',len(R),'min scale',min(r['scale'] for r in R))
