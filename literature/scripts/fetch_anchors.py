#!/usr/bin/env python3
"""Fetch exact DOI metadata and reference edges; metadata is not full-text verification."""
import concurrent.futures,hashlib,json,urllib.request,urllib.parse,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOIS='''10.1080/1047840X.2024.2384125
10.1037/0033-295X.107.2.261
10.1016/j.jml.2005.08.005
10.1111/j.1745-6916.2006.00017.x
10.1037/h0020071
10.1177/0963721413475622
10.1146/annurev-psych-010419-051101
10.1177/1470357207084865
10.1177/1750698019829891
10.1177/17506980211073093
10.1177/1461444814532062
10.1080/17503280.2020.1815123
10.1080/17503280.2024.2350603
10.1080/09658211.2024.2377193
10.1002/acp.4150
10.1177/19485506231163012
10.3389/fpsyg.2025.1574855
10.1145/2317956.2318055
10.2196/30517
10.3758/s13428-025-02767-3
10.3758/s13428-023-02145-x
10.1038/s44159-024-00312-1
10.1177/27000710241264452
10.3724/SP.J.1042.2014.00269
10.3724/SP.J.1042.2017.01713'''.splitlines()
def fetch(doi):
 folder=ROOT/'sources/crossref';folder.mkdir(parents=True,exist_ok=True)
 path=folder/(hashlib.sha256(doi.lower().encode()).hexdigest()[:16]+'.json')
 url='https://api.crossref.org/works/'+urllib.parse.quote(doi,safe='')
 try:
  if path.exists(): raw=json.loads(path.read_text())
  else:
   with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'PersonalRecallResearch/1.0'}),timeout=35) as r: raw=json.load(r)
   path.write_text(json.dumps(raw,ensure_ascii=False,indent=2))
  m=raw['message'];print(doi,m.get('title'),flush=True)
  return {'doi':doi.lower(),'status':'metadata_obtained','url':url,'date':'2026-10-23','raw':str(path.relative_to(ROOT)),'reference_count':len(m.get('reference',[]))}
 except Exception as e:
  print(doi,str(e),flush=True);return {'doi':doi.lower(),'status':'failed','error':str(e),'url':url,'date':'2026-10-23'}
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex: log=list(ex.map(fetch,DOIS))
 (ROOT/'data/anchor-access.json').write_text(json.dumps(log,ensure_ascii=False,indent=2))
 edges=[]
 for r in log:
  if r['status']!='metadata_obtained':continue
  for ref in json.loads((ROOT/r['raw']).read_text())['message'].get('reference',[]):
   edges.append({'source_doi':r['doi'],'target_doi':ref.get('DOI','').lower(),'reference':ref,'relation':'publisher_reference_metadata','evidence':r['raw'],'note':'参考文献表关系；尚未核对引文语境，不自动解释为支持或反对'})
 (ROOT/'data/publisher-reference-edges.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in edges))
 print('REFERENCES',len(edges),flush=True)
