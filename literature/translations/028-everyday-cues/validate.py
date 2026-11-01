from pathlib import Path
import fitz,json,re,hashlib
from collections import Counter
D=Path(__file__).parent;ROOT=D.resolve().parents[2]
src=fitz.open(ROOT/'literature/sources/fulltext/06-things-that-make-us-reminisce-2015.pdf');dst=fitz.open(ROOT/'output/pdf/028-日常记忆线索-中文待验收.pdf')
R=json.loads((D/'版面映射-进行中.json').read_text());F=json.loads((D/'图2版面映射.json').read_text());report={'pages':len(dst),'sizes_match':len(src)==len(dst)==10 and all(a.rect==b.rect for a,b in zip(src,dst)),'missing_chinese':{},'bibliography':[]}
assert report['sizes_match']
for i in range(10):
 expected=''.join(r['text'] for r in R if r['page']==i)+(''.join(r['text'] for r in F) if i==3 else '')
 missing=dict(Counter(re.findall(r'[\u4e00-\u9fff]',expected))-Counter(re.findall(r'[\u4e00-\u9fff]',dst[i].get_text())))
 report['missing_chinese'][str(i+1)]=missing;assert not missing,(i,missing)
for rect in [[54,158,298,717],[317,61,561,717]]:
 same=src[9].get_text(clip=fitz.Rect(rect))==dst[9].get_text(clip=fitz.Rect(rect));report['bibliography'].append(same);assert same
# PDF text overlays translate diary writing, leaving original image data and positions intact.
def ims(d):return [(i,hashlib.sha256(d.extract_image(x[0])['image']).hexdigest()) for i,p in enumerate(d) for x in p.get_images()]
report['underlying_images_preserved']=ims(src)==ims(dst);assert report['underlying_images_preserved']
report['figure2_translated_overlay_regions']=len(F);report['minimum_body_scale']=min(r['scale'] for r in R)
report['key_statistics_present']=all(x in ''.join(p.get_text() for p in dst) for x in ['208','52%','14%','51%','21%','27%','45%','40%','15%','016.128.303','2012000570'])
assert report['key_statistics_present']
(D/'最终核对.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False))
