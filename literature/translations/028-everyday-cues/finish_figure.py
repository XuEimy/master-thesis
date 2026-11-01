from pathlib import Path
import fitz,html,json
from fontTools import subset
ROOT=Path(__file__).resolve().parents[3];D=Path(__file__).parent
R=[]
def add(box,text,size=5):R.append(dict(box=box,text=text,size=size))
add([343,62,817,914],'日期：2014年3月27日\n时间：下午6:30；地点：妈妈家\n\n【简要描述被唤起的记忆】\n我想起了……\nlalalalalalalal\n童年的生日蛋糕。\n想起小时候我吃过的各种蛋糕，以及兄弟的蛋糕。还想起装饰、布置派对、筹划，以及当时特别兴奋的心情。期待。喜悦。\n\n【简要描述或画出使你回想的事物】\n因为我注意到……\n翻阅一本经典生日蛋糕食谱，并为侄女筹划生日。\n\n【简要描述回想对你的影响】\n这使我感到……\n感伤，怀旧。希望我的侄女和侄子也能拥有同样的喜悦和幸福。',5)
add([922,108,1434,202],'日期：2014年3月28日；时间：下午1点；地点：我家\n【简要描述被唤起的记忆】我想起了……',4.5)
add([925,213,1230,480],'抽奖没有中奖。\n\n参观MCA的\n小野洋子展览。',5)
add([911,498,1425,551],'【简要描述或画出使你回想的事物】',4.5)
add([907,557,1171,708],'因为我注意到……\n我找到了物件：\n未中奖的抽奖票；\n来自小野洋子作品的一块拼图片。',4.5)
add([890,722,1433,980],'【简要描述回想对你的影响】\n这使我感到……\n没有中奖——有些沮丧，因为我从来没有抽奖中过奖。同时也很高兴，因为我并不想要那个奖品。\n小野洋子——想象那个空间、那些房间和其他作品；感到受到启发。',4.5)
opt=subset.Options();f=subset.load_font(str(ROOT/'tmp/pdfs/songti.ttf'),opt);ss=subset.Subsetter(options=opt);ss.populate(text=''.join(r['text'] for r in R));ss.subset(f);subset.save_font(f,str(ROOT/'tmp/pdfs/028-figure-songti.ttf'),opt)
d=fitz.open(ROOT/'output/pdf/028-日常记忆线索-中文排版草稿.pdf');p=d[3]
def xy(x,y):return fitz.Point(53.99976+x*242.64/1500,274.080017+y*166.8/1030)
def rect(b):return fitz.Rect(xy(*b[:2]),xy(*b[2:]))
# Add translated PDF text over printed / handwritten portions; keep the diary edges,
# ticket and blue puzzle piece in their original positions.
polys=[[(335,52),(855,100),(821,926),(315,889)],[(910,104),(1450,122),(1450,206),(910,206)],[(916,207),(1254,207),(1254,495),(916,495)],[(896,497),(1432,497),(1432,553),(896,553)],[(898,555),(1187,555),(1187,717),(898,717)],[(875,718),(1454,718),(1454,989),(875,989)]]
for poly in polys:
 sh=p.new_shape();sh.draw_polyline([xy(*x) for x in poly]);sh.finish(color=None,fill=(.87,.88,.91),closePath=True);sh.commit()
for box in [[335,48,855,130],[888,102,1452,206],[880,495,1435,555],[1180,549,1318,616],[845,710,1455,989]]:
 p.draw_rect(rect(box),color=None,fill=(.87,.88,.91))
for r in R:
 r['rect']=list(rect(r['box']));sp,sc=p.insert_htmlbox(rect(r['box']),'<p>'+html.escape(r['text']).replace('\n','<br>')+'</p>',css="@font-face{font-family:cn;src:url('028-figure-songti.ttf')}body{font-family:cn;font-size:%spt;margin:0}p{margin:0;line-height:1.15}"%r['size'],archive=fitz.Archive(str(ROOT/'tmp/pdfs')),scale_low=.85);r.update(spare=sp,scale=sc);assert sp>=0,r
out=ROOT/'output/pdf/028-日常记忆线索-中文待验收.pdf';d.save(out,garbage=3,deflate=True);d.close();d=fitz.open(out)
(D/'图2版面映射.json').write_text(json.dumps(R,ensure_ascii=False,indent=2))
d[3].get_pixmap(matrix=fitz.Matrix(2,2)).save('/tmp/028-figure-finished.png');d[3].get_pixmap(matrix=fitz.Matrix(4,4),clip=fitz.Rect(54,274,297,441)).save('/tmp/028-figure-detail.png')
print(out,[(r['spare'],r['scale']) for r in R])
