#!/usr/bin/env python3
import concurrent.futures,json,urllib.request,xml.etree.ElementTree as ET
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def fetch(pmc):
 url='https://www.ebi.ac.uk/europepmc/webservices/rest/'+pmc+'/fullTextXML';folder=R/'sources/fulltext';folder.mkdir(exist_ok=True)
 record={'pmcid':pmc,'url':url,'date':'2026-10-23'}
 try:
  path=folder/(pmc+'.xml')
  if path.exists():raw=path.read_bytes()
  else:
   with urllib.request.urlopen(url,timeout=40) as r:raw=r.read()
   path.write_bytes(raw)
  root=ET.fromstring(raw);body=root.find('body')
  if body is None:raise ValueError('No article body; not treated as full text')
  paras=[]
  def walk(el,section):
   if el.tag=='sec':section=section+[ ''.join(el.find('title').itertext()).strip() if el.find('title') is not None else el.get('id','') ]
   if el.tag in ['p','table-wrap','fig']:
    paras.append({'paragraph':len(paras)+1,'section':section,'text':' '.join(''.join(el.itertext()).split())});return
   for child in el:
    if child.tag!='title':walk(child,section)
  walk(body,[])
  abstract=root.find('front/article-meta/abstract');title=root.find('front/article-meta/title-group/article-title')
  obj={'title':''.join(title.itertext()) if title is not None else '', 'abstract':''.join(abstract.itertext()) if abstract is not None else '', 'paragraphs':paras,'reference_count':len(root.findall('.//ref-list/ref'))}
  jp=folder/(pmc+'.json');jp.write_text(json.dumps(obj,ensure_ascii=False,indent=2));record.update(status='全文获取，尚未核读',path=str(path.relative_to(R)),parsed=str(jp.relative_to(R)),paragraphs=len(paras))
 except Exception as e:record.update(status='failed',error=str(e))
 print(json.dumps(record,ensure_ascii=False),flush=True);return record
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:rr=list(pool.map(fetch,['PMC7741080','PMC9296013','PMC13679482']))
 (R/'data/pmc-fulltext-access.json').write_text(json.dumps(rr,ensure_ascii=False,indent=2))
