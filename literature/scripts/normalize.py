#!/usr/bin/env python3
"""Normalize metadata preserving each source and query; heuristic tags are NOT eligibility decisions."""
import csv, hashlib, html, json, re, unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def clean(x):return re.sub('<[^>]+>',' ',html.unescape(str(x or ''))).strip()
def titlekey(t):return ''.join(c for c in unicodedata.normalize('NFKC',t).lower() if c.isalnum())
def doi(x):return re.sub(r'^https?://(dx\.)?doi.org/','',str(x or '').strip(),flags=re.I).lower()
def base(provider,r):
 if provider in ('pubmed','arxiv','doaj'):
  out=dict(r);out['title']=clean(r.get('title'));out['doi']=doi(r.get('doi'));out['abstract']=clean(r.get('abstract'));return out
 if provider=='semanticscholar':
  ex=r.get('externalIds') or {};oa=r.get('openAccessPdf') or {}
  return dict(title=clean(r.get('title')),doi=doi(ex.get('DOI')),authors=[a.get('name') for a in r.get('authors',[])],year=r.get('year'),date=r.get('publicationDate'),venue=r.get('venue'),publication_type=r.get('publicationTypes'),abstract=clean(r.get('abstract')),url=r.get('url'),provider_id=r.get('paperId'),ids=ex,fulltext_urls=[oa['url']] if oa.get('url') else [],reference_ids=[],citation_count=r.get('citationCount'))
 if provider=='europepmc':
  ji=r.get('journalInfo') or {};j=ji.get('journal') or {};urls=r.get('fullTextUrlList',{}).get('fullTextUrl',[])
  return dict(title=clean(r.get('title')),doi=doi(r.get('doi')),authors=[a.get('fullName') for a in r.get('authorList',{}).get('author',[])],year=r.get('pubYear'),date=r.get('firstPublicationDate'),venue=j.get('title'),publication_type=r.get('pubTypeList',{}).get('pubType'),abstract=clean(r.get('abstractText')),url='https://europepmc.org/article/'+str(r.get('source'))+'/'+str(r.get('id')),provider_id=r.get('id'),ids={'PMID':r.get('pmid'),'PMCID':r.get('pmcid')},fulltext_urls=[u.get('url') for u in urls if u.get('url') and u.get('availability') in ['Open access','Free']],reference_ids=[],citation_count=r.get('citedByCount'))
 inv=r.get('abstract_inverted_index') or {};pairs=sorted((p,w) for w,pp in inv.items() for p in pp);loc=r.get('primary_location') or {};source=loc.get('source') or {}
 return dict(title=clean(r.get('title')),doi=doi(r.get('doi')),authors=[a.get('author',{}).get('display_name') for a in r.get('authorships',[])],year=r.get('publication_year'),date=r.get('publication_date'),venue=source.get('display_name'),publication_type=r.get('type'),abstract=' '.join(w for p,w in pairs),url=loc.get('landing_page_url') or r.get('id'),provider_id=r.get('id'),ids={'OpenAlex':r.get('id')},fulltext_urls=list(dict.fromkeys(l['pdf_url'] for l in r.get('locations',[]) if l.get('pdf_url'))),reference_ids=r.get('referenced_works',[]),citation_count=r.get('cited_by_count'))
records=[];searches=[]
for folder in sorted((ROOT/'sources/api').iterdir()):
 if not folder.is_dir() or not (folder/'search.json').exists():continue
 state=json.loads((folder/'search.json').read_text());searches.append(state);provider=state['provider']
 for page in sorted(folder.glob('page-*.json')):
  obj=json.loads(page.read_text());items=obj.get('records',[]) if provider in ('pubmed','arxiv','doaj') else obj.get('data',[]) if provider=='semanticscholar' else obj.get('resultList',{}).get('result',[]) if provider=='europepmc' else obj.get('results',[])
  for raw in items:
   r=base(provider,raw)
   if not r['title']:continue
   r['provenance']=[dict(provider=provider,search_id=state['search_id'],provider_id=r['provider_id'],raw_page=str(page.relative_to(ROOT)),query_status=state['status'])]
   r['from_pilot']=state['status']=='superseded_query';records.append(r)
merged={};bytitle={}
for r in sorted(records,key=lambda x:not bool(x['doi'])):
 tk=titlekey(r['title']);key='doi:'+r['doi'] if r['doi'] else None
 if not key:
  keys=bytitle.get(tk,set());key=next(iter(keys)) if len(keys)==1 else 'title:'+tk
 if key not in merged:
  merged[key]=r;bytitle.setdefault(tk,set()).add(key)
 else:
  m=merged[key];m['provenance']+=r['provenance'];m['from_pilot']=m['from_pilot'] and r['from_pilot']
  for k in ['abstract','authors','venue','publication_type','year','date']:
   if not m.get(k) or (k=='abstract' and len(r.get(k) or '')>len(m.get(k) or '')):m[k]=r.get(k)
  for k in ['fulltext_urls','reference_ids']:m[k]=list(dict.fromkeys(m[k]+r[k]))
  m['ids'].update({k:v for k,v in r['ids'].items() if v})
TAGS={
'记忆机制':r'autobiograph|episodic memory|involuntary memor|retrieval cue|self.memory|encoding specificity',
'认知神经与事件':r'hippocamp|neural|neuroimag|event segment|event boundar|naturalistic memory|context reinstatement',
'感官与情绪线索':r'music.evoked|odou?r|olfact|multisensory|sensory modal|emotional autobiograph|nostalgia',
'叙事与身份':r'narrative identity|autobiographical reasoning|life stor|life writ|autobiograph.*narrat|self.defining',
'摄影与记录':r'photo|camera|lifelog|sensecam|wearable|egocentric',
'纪录片与视觉方法':r'documentary|home movies|photo.elicitation|visual anthrop|sensory ethnograph|autobiographical film',
'媒介与传播':r'mediated memor|digital memor|algorithmic memor|social media|personal archive|digital photograph',
'设计与交互':r'design|human.computer|personal informatics|ritual|serendip|souvenir|tangible',
'AI与计算实现':r'artificial intelligence|generative|language model|computer vision|lifelog retrieval|video summar',
'回忆干预与评估':r'reminiscence|life review|autobiographical interview|memory characteristics|memory questionnaire|sensecam',
'真实性与反例':r'false memor|misinformation|source monitoring|photo.taking.impair|distort|forgetting'
}
result=[]
for key,r in merged.items():
 r['id']='L'+hashlib.sha256(key.encode()).hexdigest()[:12]
 tx=(r['title']+' '+r['abstract']).lower();r['tags']=[k for k,p in TAGS.items() if re.search(p,tx)]
 r['screening_status']='未人工筛选';r['fulltext_status']='尚未尝试';r['evidence_level']='元数据及摘要可得，尚未核读' if r['abstract'] else '仅元数据'
 r['link_priority']=sum(bool(re.search(p,r['title'].lower())) for p in [r'autobiograph|reminiscence|remembering|personal memor',r'photo|camera|lifelog|cue|digital|generative|narrat|documentary',r'review|model|framework'])
 if r['from_pilot']:r['screening_status']='先导宽检索，未人工筛选'
 if r.get('date') and str(r['date'])>'2026-10-23':r['screening_status']='待核对出版日期是否超出截止日'
 result.append(r)
result.sort(key=lambda r:(-r['link_priority'],-int(r.get('year') or 0),r['title']))
(ROOT/'data/records.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in result))
(ROOT/'data/search-log.json').write_text(json.dumps(searches,ensure_ascii=False,indent=2))
with (ROOT/'data/文献总库.csv').open('w',newline='',encoding='utf-8-sig') as f:
 cols=['id','title','authors','year','date','venue','publication_type','doi','url','tags','screening_status','evidence_level','fulltext_status','fulltext_urls']
 w=csv.DictWriter(f,fieldnames=cols);w.writeheader()
 for r in result:w.writerow({k:'; '.join(str(x) for x in r[k]) if isinstance(r.get(k),list) else r.get(k) for k in cols})
summary={'raw_records':len(records),'unique_reports':len(result),'searches':len(searches),'complete_searches':sum(s['status']=='complete' for s in searches),'incomplete_searches':sum(s['status']!='complete' for s in searches),'screened_studies':None,'note':'候选报告数，不是纳入研究数；自动标签和排序不构成人工筛选。'}
(ROOT/'data/harvest-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));print(json.dumps(summary,ensure_ascii=False))
for tag in TAGS:
 candidates=[r for r in result if tag in r['tags'] and not r['from_pilot']]
 out='\n'.join(f"{r['id']} | {r.get('year')} | {r['title']} | {r.get('doi')}" for r in candidates)
 (ROOT/'data'/('候选-'+tag+'.txt')).write_text(out)
