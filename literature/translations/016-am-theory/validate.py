from pathlib import Path
import fitz,json,re,hashlib,shutil
from collections import Counter
D=Path(__file__).parent;ROOT=D.resolve().parents[2]
src=fitz.open(ROOT/'literature/sources/fulltext/02-van-den-hoven-eggen-2008-augmented-memory-am-theory.pdf');draft=ROOT/'output/pdf/016-自传体记忆理论与增强记忆设计-中文排版草稿.pdf';dst=fitz.open(draft)
R=json.loads((D/'版面映射-进行中.json').read_text());report={'pages':len(dst),'sizes_match':all(a.rect==b.rect for a,b in zip(src,dst)),'missing_chinese':{},'bibliography':[]}
assert len(src)==len(dst)==11
for i in range(11):
 expected=Counter(re.findall(r'[\u4e00-\u9fff]',''.join(r['text'] for r in R if r['page']==i)));actual=Counter(re.findall(r'[\u4e00-\u9fff]',dst[i].get_text()));missing=dict(expected-actual);report['missing_chinese'][str(i+1)]=missing;assert not missing,(i,missing)
for i,r in [(9,[306,168,545,720]),(10,[51,58,290,628]),(10,[306,58,545,588])]:
 eq=src[i].get_text(clip=fitz.Rect(r))==dst[i].get_text(clip=fitz.Rect(r));report['bibliography'].append(eq);assert eq
# Every support mark in the original table must retain the exact character and position.
def marks(p):return [(tuple(round(v,3) for v in w[:4]),w[4]) for w in p.get_text('words') if 78<w[1]<232 and w[0]>313]
report['table_marks_preserved']=len(marks(src[5]))==len(marks(dst[5])) and all(a[1]==b[1] and max(abs(x-y) for x,y in zip(a[0],b[0]))<0.01 for a,b in zip(marks(src[5]),marks(dst[5])));report['table_mark_count']=len(marks(src[5]));assert report['table_marks_preserved']
def images(d):return [hashlib.sha256(d.extract_image(x[0])['image']).hexdigest() for p in d for x in p.get_images()]
report['images_preserved']=images(src)==images(dst);assert report['images_preserved']
report['minimum_insert_scale']=min(r['scale'] for r in R)
(D/'最终核对.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False))
