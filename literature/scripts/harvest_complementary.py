#!/usr/bin/env python3
"""Complementary PubMed, arXiv, DOAJ searches; retain queries, raw pages and all matches.
Each provider has its own sequential request stream; do not conflate records with studies.
"""
import concurrent.futures,datetime,hashlib,json,re,time,urllib.parse,urllib.request,xml.etree.ElementTree as ET
from pathlib import Path
R=Path(__file__).resolve().parents[1];END='2026-10-23'
QUERIES={
'pubmed':[
'(autobiographical[Title/Abstract] OR episodic[Title/Abstract]) AND (photograph*[Title/Abstract] OR SenseCam[Title/Abstract] OR lifelog*[Title/Abstract] OR "wearable camera"[Title/Abstract])',
'"autobiographical memory"[Title/Abstract] AND (cue*[Title/Abstract] OR involuntary[Title/Abstract] OR retrieval[Title/Abstract])',
'"autobiographical memory"[Title/Abstract] AND (narrative[Title/Abstract] OR identity[Title/Abstract] OR "self-memory"[Title/Abstract])',
'(reminiscence[Title/Abstract] OR "autobiographical memory"[Title/Abstract]) AND (digital[Title/Abstract] OR "artificial intelligence"[Title/Abstract] OR generative[Title/Abstract])',
'("event boundaries"[Title/Abstract] OR "event segmentation"[Title/Abstract]) AND (memory[Title/Abstract] OR remembering[Title/Abstract])',
'"photo-taking"[Title/Abstract] AND (memory[Title/Abstract] OR experience[Title/Abstract])',
'"autobiographical memory"[Title/Abstract] AND (music[Title/Abstract] OR odor[Title/Abstract] OR odour[Title/Abstract] OR sensory[Title/Abstract])',
'"Memory, Episodic"[MeSH Terms] AND (photograph*[Title/Abstract] OR reminiscence[Title/Abstract] OR "daily life"[Title/Abstract])'
],
'arxiv':[
'all:lifelogging OR all:SenseCam',
'all:"autobiographical memory"',
'(ti:reminiscence OR abs:reminiscence) AND (abs:autobiographical OR abs:older OR abs:dementia OR abs:personal OR abs:recollection)',
'all:"false memories" AND (all:generative OR all:AI OR all:chatbot)',
'all:"personal memory" AND (all:photo OR all:video OR all:multimodal)',
'all:"egocentric video" AND (all:memory OR all:retrieval OR all:summarization)',
'all:"event segmentation" AND (all:episodic OR all:autobiographical)'
],
'doaj':[
'bibjson.title:"autobiographical memory"',
'bibjson.title:lifelogging',
'bibjson.title:reminiscence AND (bibjson.title:digital OR bibjson.title:technology OR bibjson.title:AI)',
'bibjson.title:"photo-elicitation"',
'bibjson.title:"narrative identity"',
'bibjson.title:"digital memory"',
'bibjson.title:"autobiographical documentary"',
'bibjson.title:"sensory ethnography"',
'bibjson.title:"mediated memory"'
]}
def save(p,obj):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2))
def request(url,wait):
 time.sleep(wait)
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'PersonalRecallResearch/1.0'}),timeout=50) as r:return r.read()
def common(title,doi='',authors=None,year=None,date=None,venue='',abstract='',url='',pid='',ids=None,full=None,ptype=None):
 return dict(title=title,doi=doi,authors=authors or [],year=year,date=date,venue=venue,abstract=abstract,url=url,provider_id=pid,ids=ids or {},fulltext_urls=full or [],publication_type=ptype,reference_ids=[],citation_count=None)
def text(el):return ''.join(el.itertext()).strip() if el is not None else ''
def pubmed(q,folder,state):
 term='('+q+') AND ("1900/01/01"[Date - Publication] : "2026/10/23"[Date - Publication])';state['effective_query']=term;state['date_filter']='PubMed Date - Publication'
 # Queries here are under the API ceiling; above-ceiling queries remain incomplete for date partitioning.
 url='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?'+urllib.parse.urlencode(dict(db='pubmed',term=term,retmode='json',retmax=9999,tool='personal_recall_literature'))
 sp=folder/'esearch.json';o=json.loads(sp.read_text()) if sp.exists() else json.loads(request(url,.4));save(sp,o)
 sr=o['esearchresult'];state['query_translation']=sr.get('querytranslation');state['warnings']=sr.get('warninglist');state['total']=int(sr['count']);state['last_url']=url
 if state['total']>9999:raise RuntimeError('Needs date partition: PubMed >9999 matches; not declared complete')
 ids=sr['idlist'];seen=set()
 for start in range(0,len(ids),200):
  n=start//200+1;rawpath=folder/f'raw-{n:04}.xml';part=ids[start:start+200]
  url='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?'+urllib.parse.urlencode(dict(db='pubmed',id=','.join(part),retmode='xml',tool='personal_recall_literature'))
  raw=rawpath.read_bytes() if rawpath.exists() else request(url,.4);rawpath.write_bytes(raw);tree=ET.fromstring(raw);items=[]
  for a in list(tree):
   pmid=text(a.find('.//PMID'));title=text(a.find('.//ArticleTitle'));art=a.find('.//Article');art=art if art is not None else a.find('.//BookDocument')
   if not pmid or art is None:continue
   journal=text(art.find('.//Journal/Title'));authors=[]
   for au in art.findall('.//AuthorList/Author'):
    name=(text(au.find('ForeName'))+' '+text(au.find('LastName'))).strip() or text(au.find('CollectiveName'))
    if name:authors.append(name)
   doi='';ext={'PMID':pmid}
   for i in a.findall('./PubmedData/ArticleIdList/ArticleId') + a.findall('./PubmedBookData/ArticleIdList/ArticleId'):
    ty=i.get('IdType');v=text(i)
    if ty=='doi':doi=v
    elif ty=='pmc':ext['PMCID']=v
   if not doi:
    doi=next((text(i) for i in art.findall('./ELocationID') if i.get('EIdType')=='doi'), '')
   dp=art.find('.//JournalIssue/PubDate');yr=text(dp.find('Year')) if dp is not None else ''
   if not yr and dp is not None:
    m=re.search(r'\d{4}',text(dp));yr=m.group() if m else ''
   abstract=' '.join(text(x) for x in art.findall('.//Abstract/AbstractText'))
   full=['https://pmc.ncbi.nlm.nih.gov/articles/'+ext['PMCID']+'/'] if ext.get('PMCID') else []
   items.append(common(title,doi,authors,int(yr) if yr else None,venue=journal,abstract=abstract,url='https://pubmed.ncbi.nlm.nih.gov/'+pmid+'/',pid=pmid,ids=ext,full=full,ptype=[text(x) for x in art.findall('.//PublicationType')]))
   seen.add(pmid)
  save(folder/f'page-{n:04}.json',{'records':items,'requested_ids':part,'source_url':url})
  state.update(retrieved=len(seen),pages=n,last_url=url);save(folder/'search.json',state)
 if seen!=set(ids):raise RuntimeError('Requested/returned PubMed IDs mismatch '+str(len(set(ids)-seen)))
 state['status']='complete'
def arxiv(q,folder,state):
 ns={'a':'http://www.w3.org/2005/Atom','o':'http://a9.com/-/spec/opensearch/1.1/','x':'http://arxiv.org/schemas/atom'};start=0;n=0
 effective='('+q+') AND submittedDate:[199101010000 TO 202610232359]';state['effective_query']=effective;state['date_filter']='arXiv original submittedDate UTC cutoff; version updated date preserved'
 while True:
  n+=1;url='https://export.arxiv.org/api/query?'+urllib.parse.urlencode(dict(search_query=effective,start=start,max_results=1000,sortBy='submittedDate',sortOrder='ascending'))
  rawpath=folder/f'raw-{n:04}.xml';raw=rawpath.read_bytes() if rawpath.exists() else request(url,3.1);rawpath.write_bytes(raw);root=ET.fromstring(raw)
  total=root.find('o:totalResults',ns)
  if total is None:raise RuntimeError('Missing arXiv total, possible API error')
  state['total']=int(total.text);items=[]
  for e in root.findall('a:entry',ns):
   pid=text(e.find('a:id',ns));title=text(e.find('a:title',ns))
   if '/errors' in pid:raise RuntimeError(text(e.find('a:summary',ns)))
   published=text(e.find('a:published',ns));updated=text(e.find('a:updated',ns));doi=text(e.find('x:doi',ns))
   item=common(title,doi,[text(a.find('a:name',ns)) for a in e.findall('a:author',ns)],int(published[:4]) if published else None,published[:10],text(e.find('x:journal_ref',ns)),text(e.find('a:summary',ns)),pid,pid,{'arXiv':pid,'arXiv_updated':updated},[l.get('href') for l in e.findall('a:link',ns) if l.get('title')=='pdf'],'preprint')
   # Publisher DOI is a relation, not this preprint's report identity.
   item['ids']['publisher_DOI']=doi;item['doi']='10.48550/arxiv.'+pid.rsplit('/',1)[-1].split('v')[0] if '/abs/' in pid else ''
   items.append(item)
  save(folder/f'page-{n:04}.json',{'records':items,'source_url':url});start+=len(items);state.update(retrieved=start,pages=n,last_url=url);save(folder/'search.json',state)
  if start>=state['total']:state['status']='complete';return
  if not items:raise RuntimeError('Empty arXiv page before total')
  if start>=30000:raise RuntimeError('Needs arXiv partition beyond 30000')
def doaj(q,folder,state):
 page=1;got=0;state['date_filter']='No API publication-date filter; exact dates screened against 2026-10-23'
 while True:
  url='https://doaj.org/api/search/articles/'+urllib.parse.quote(q,safe='')+'?'+urllib.parse.urlencode({'page':page,'pageSize':100})
  rawpath=folder/f'raw-{page:04}.json';o=json.loads(rawpath.read_text()) if rawpath.exists() else json.loads(request(url,.5));save(rawpath,o)
  state['total']=o['total'];items=[]
  for r in o['results']:
   b=r['bibjson'];ident=b.get('identifier',[]);doi=next((i['id'] for i in ident if i.get('type')=='doi'),'');pid=r['id'];links=b.get('link',[])
   year=b.get('year');items.append(common(b.get('title',''),doi,[a.get('name','') for a in b.get('author',[])],int(year) if str(year).isdigit() else None,None,b.get('journal',{}).get('title',''),b.get('abstract',''),'https://doaj.org/article/'+pid,pid,{'DOAJ':pid},[l['url'] for l in links if l.get('type')=='fulltext'],'journal-article'))
  save(folder/f'page-{page:04}.json',{'records':items,'source_url':url});got+=len(items);state.update(retrieved=got,pages=page,last_url=url);save(folder/'search.json',state)
  if got>=state['total']:state['status']='complete';return
  if not items:raise RuntimeError('Empty DOAJ page before total')
  page+=1

def run(provider):
 for q in QUERIES[provider]:
  sid=provider+'-'+hashlib.sha256(q.encode()).hexdigest()[:12];folder=R/'sources/api'/sid;folder.mkdir(parents=True,exist_ok=True);p=folder/'search.json'
  state=json.loads(p.read_text()) if p.exists() else dict(search_id=sid,provider=provider,query=q,search_date=END,status='pending',retrieved=0,pages=0,records_vs_studies='records')
  if state['status']=='complete':print(sid,'cached',state['retrieved'],flush=True);continue
  try:globals()[provider](q,folder,state)
  except Exception as e:state.update(status='failed',error=str(e))
  save(p,state);print(sid,state['status'],state['retrieved'],'of',state.get('total'),state.get('error',''),flush=True)
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(run,QUERIES))
