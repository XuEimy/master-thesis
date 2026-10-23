#!/usr/bin/env python3
"""Run the literature-review skill verifier concurrently, preserving uncertainty."""
import sys,json,concurrent.futures
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,'/Users/EimyXu/.codex/skills/literature-review/scripts')
from verify_citations import CitationVerifier
# Adjacent Markdown citations can be greedily merged by the bundled extractor.
# Use the audited ledger's exact identifiers, then verify those with the skill API.
dois=[r['doi'] for r in json.loads((R/'review/citation-ledger.json').read_text()) if r.get('doi')]
cache_path=R/'review/doi-verification.json'
cache={x['doi']:x for x in json.loads(cache_path.read_text())['results'] if x['doi'] in dois and x['registration_confirmed']} if cache_path.exists() else {}
def check(d):
 if d in cache:return cache[d]
 ok,m=CitationVerifier().verify_doi(d)
 print(d,m.get('status'),flush=True)
 return {'doi':d,'registration_confirmed':ok,'result':m}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:results=list(ex.map(check,dois))
for x in results:x['result'].pop('crossref_message',None)
(R/'review/doi-verification.json').write_text(json.dumps({'date':'2026-10-23','script':'literature-review/scripts/verify_citations.py','identifier_source':'citation-ledger.json 精确标识；避开通用正则对相邻 Markdown 链接的误提取','note':'注册检查不能证明论点支持；网络失败保留为不确定。精确元数据另存 sources/crossref。','results':results},ensure_ascii=False,indent=2))
print('DONE',len(results),sum(x['registration_confirmed'] for x in results),flush=True)
