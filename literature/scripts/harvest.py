#!/usr/bin/env python3
"""Resumeable public bibliographic harvesting. Preserve raw pages and exact queries.
No result-count cap; each query follows provider continuation until exhausted.
Failures remain explicit and resumable. No keys or credentials recorded.
"""
import argparse, concurrent.futures, datetime, hashlib, json, time, urllib.request, urllib.parse, urllib.error
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
END='2026-10-23'
QUERIES={
'semanticscholar':[
'"lifelogging" | "SenseCam"',
'"autobiographical memory" + (photograph | photographs | photo | photos | camera | cameras)',
'"autobiographical memory" + (cue | cues | cueing | retrieval)',
'reminiscence + (digital | technology | technologies | "artificial intelligence" | generative)',
'"personal memory" + (design | digital | technology | capture)',
'"photo-taking" + memory',
'"PhotoUse" | "Photobox" | "Story Shell"',
'"event segmentation" + memory',
'("generative AI" | "generative artificial intelligence") + (autobiographical | reminiscence | "false memories" | remembering)',
'"memory cues" + (design | personal | multimodal)',
'"involuntary autobiographical memories" + (cue | cues | everyday | digital)',
'"episodic memory" + (wearable | lifelog | "egocentric video")',
'"personal informatics" + (capture | habit | reflection | remembering)',
'reminiscence + (ritual | serendipity | notification)',
'"life review" + ("artificial intelligence" | photograph | digital)',
'"autobiographical memory" + (narrative | identity | "self-memory")'
],
'europepmc':[
'(lifelogging OR SenseCam OR "wearable camera")',
'"autobiographical memory" AND (photograph* OR photo OR photos OR video OR camera)',
'"autobiographical memory" AND (cue OR cues OR cueing OR multimodal OR sensory)',
'reminiscence AND (digital OR technology OR "artificial intelligence" OR generative)',
'"photo-taking" AND memory',
'"event segmentation" AND memory',
'("generative AI" OR "generative artificial intelligence") AND (memory OR reminiscence)',
'"involuntary autobiographical" AND (everyday OR cue OR cues)',
'"autobiographical memory" AND (narrative OR identity OR "self-memory")'
],
'openalex':[
'"lifelogging" "memory"',
'"autobiographical memory" "photographs"',
'"reminiscence" "design"',
'"generative" "reminiscence"',
'"photo-taking" "memory"',
'"personal informatics" "reflection"',
'"autobiographical memory" "cues"',
'"memory" "Photobox"'
]}
def write(path,obj):
 path.parent.mkdir(parents=True,exist_ok=True)
 tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(json.dumps(obj,ensure_ascii=False,indent=2));tmp.replace(path)
def get(url):
 for attempt in range(3):
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'PersonalRecallLiterature/1.0 (academic read-only)'}),timeout=60) as r:
    return json.load(r)
  except urllib.error.HTTPError as e:
   if e.code in (429,500,502,503,504) and attempt<2: time.sleep((5,15)[attempt]);continue
   raise
  except (TimeoutError,urllib.error.URLError):
   if attempt<2: time.sleep(3);continue
   raise

def run(provider):
 for n,q in enumerate(QUERIES[provider],1):
  qid=provider+'-'+hashlib.sha256(q.encode()).hexdigest()[:12]
  folder=ROOT/'sources/api'/qid; folder.mkdir(parents=True,exist_ok=True)
  statepath=folder/'search.json'
  state=json.loads(statepath.read_text()) if statepath.exists() else {'search_id':qid,'provider':provider,'query':q,'search_date':END,'retrieved':0,'pages':0,'status':'pending','records_vs_studies':'records','date_filter':'publication year <= 2026; exact dates screened against 2026-10-23'}
  if state['status']=='complete':print(qid,'cached complete',state['retrieved'],flush=True);continue
  cursor=state.get('next_cursor','*' if provider!='semanticscholar' else None)
  try:
   while True:
    if provider=='semanticscholar':
     params={'query':q,'year':'-2026','fields':'title,authors,year,publicationDate,venue,publicationVenue,externalIds,abstract,url,openAccessPdf,publicationTypes,citationCount,referenceCount'}
     if cursor:params['token']=cursor
     url='https://api.semanticscholar.org/graph/v1/paper/search/bulk?'+urllib.parse.urlencode(params)
    elif provider=='europepmc':
     params={'query':'('+q+') AND FIRST_PDATE:[1900-01-01 TO '+END+']','format':'json','resultType':'core','pageSize':1000,'cursorMark':cursor}
     url='https://www.ebi.ac.uk/europepmc/webservices/rest/search?'+urllib.parse.urlencode(params)
    else:
     params={'search':q,'filter':'to_publication_date:'+END,'per_page':100,'cursor':cursor,'select':'id,doi,title,publication_year,publication_date,authorships,primary_location,locations,type,abstract_inverted_index,referenced_works,cited_by_count,open_access'}
     url='https://api.openalex.org/works?'+urllib.parse.urlencode(params)
    raw=get(url)
    if provider=='semanticscholar': records=raw.get('data',[]);total=raw.get('total');nxt=raw.get('token')
    elif provider=='europepmc':records=raw.get('resultList',{}).get('result',[]);total=raw.get('hitCount');nxt=raw.get('nextCursorMark')
    else:records=raw.get('results',[]);total=raw.get('meta',{}).get('count');nxt=raw.get('meta',{}).get('next_cursor')
    if total is None:raise ValueError('Missing total in response: '+str(raw)[:200])
    page=state['pages']+1
    write(folder/f'page-{page:04d}.json',raw)
    state.update({'reported_total':total,'retrieved':state['retrieved']+len(records),'pages':page,'next_cursor':nxt,'last_url':url,'status':'running'})
    if not records or not nxt or nxt==cursor or state['retrieved']>=total:
     state['status']='complete' if state['retrieved']>=total else 'ended_before_total'
     write(statepath,state);print(qid,state['status'],state['retrieved'],'/',total,flush=True);break
    write(statepath,state);cursor=nxt
    print(qid,'page',page,state['retrieved'],'/',total,flush=True)
    time.sleep(1.3)
  except Exception as e:
   state.update({'status':'failed','error':str(e)});write(statepath,state);print(qid,'FAILED',str(e),flush=True)
  time.sleep(1.5)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('providers',nargs='*',default=list(QUERIES));args=parser.parse_args()
 with concurrent.futures.ThreadPoolExecutor(max_workers=len(args.providers)) as pool:
  list(pool.map(run,args.providers))
