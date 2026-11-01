from pathlib import Path
import fitz,json,re,collections,shutil
ROOT=Path(__file__).resolve().parents[3];D=Path(__file__).parent
s=fitz.open(ROOT/'literature/sources/fulltext/01-sellen-whittaker-2010-beyond-total-capture.pdf');path=ROOT/'output/pdf/001-超越全量记录-中文排版草稿.pdf';d=fitz.open(path)
R=json.loads((D/'版面映射-进行中.json').read_text());expected=['' for _ in d]
for r in R:expected[r['page']]+=r['text']
c=lambda x:collections.Counter(re.findall('[\u4e00-\u9fff]',x))
report={'pages':len(d),'sizes_match':all(a.rect==b.rect for a,b in zip(s,d)),'missing_chinese':[dict(c(t)-c(p.get_text())) for p,t in zip(d,expected)],'reference_regions':[],'image_digests_match':[]}
for box in [[214,454,379,741],[387,51,552,654]]:
 a=s[7].get_text(clip=fitz.Rect(box));b=d[7].get_text(clip=fitz.Rect(box));report['reference_regions'].append(a==b)
for a,b in zip(s,d):report['image_digests_match'].append([i['digest'].hex() for i in a.get_image_info(hashes=True)]==[i['digest'].hex() for i in b.get_image_info(hashes=True)])
assert report['sizes_match'] and not any(report['missing_chinese']) and all(report['reference_regions']) and all(report['image_digests_match']),report
out=ROOT/'output/pdf/001-超越全量记录-中文原版式译本.pdf';shutil.copyfile(path,out)
report['output']=str(out);report['bytes']=out.stat().st_size
(D/'最终核对.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(report)
