#!/usr/bin/env python3
"""Render the authored review with exact cached metadata and an evidence ledger."""
import json,re,csv,html
from pathlib import Path
R=Path(__file__).resolve().parents[1];P=R.parent
source=R/'review/正文底稿.md'
s=source.read_text().replace('Tullis 与 Fraundorf','Tullis 与 Finley').replace('van den Hoven 等关于日常回忆线索','van Gennip 等关于日常回忆线索')
source.write_text(s)
rr={r['doi']:r for r in map(json.loads,(R/'data/curated-records.jsonl').open())}
manual={r['id']:r for r in json.loads((R/'review/manual-sources.json').read_text())}
keys=list(dict.fromkeys(re.findall(r'\{\{cite:(.*?)\}\}',s)))
meta={}
for p in (R/'sources/crossref').glob('*.json'):
 m=json.loads(p.read_text())['message'];meta[m['DOI'].lower()]=m
def clean(t):return re.sub('<[^>]*>','',html.unescape(t or '')).strip()
refs=[];audit=[]
for i,k in enumerate(keys,1):
 if k in rr:
  r=rr[k];m=meta[k];dt=m.get('published-print') or m.get('published-online') or m.get('published');year=dt['date-parts'][0][0]
  # Publisher issue evidence overrides Crossref's earliest-date-only field.
  if k=='10.1108/oir-03-2018-0108':year=2020
  if k=='10.23991/ef.v51i2.142184':year=2024
  vol=m.get('volume','');issue=m.get('issue','');page=m.get('page') or m.get('article-number','')
  venue=clean('; '.join(r['venue']));details=vol+('('+issue+')' if issue else '')
  if page:details+=(':' if details else 'pp. ')+page
  title=r['title'];authors='; '.join(r['authors']);url='https://doi.org/'+k
  end='' if title.endswith(('.', '?', '!')) else '.'
  ref=f'{authors}. {title}{end} {venue}, {year}'+(', '+details if details else '')+f'. [DOI]({url}).'
  entry=dict(r);entry.update(reference_number=i,reference_year=year,url=url)
  entry['metadata_checks']={'identity':'精确 DOI 元数据匹配','date_policy':'优先卷期年；没有卷期年时使用网络首发年；DOI 后缀不是年份'}
  if k=='10.23991/ef.v51i2.142184':ref+='〔卷期标注 2024；在线发布 2025-02-04。〕'
  if k=='10.1108/oir-03-2018-0108':ref+='〔在线首发 2019；采用出版社卷期年 2020。〕'
  if k=='10.1145/3772318.3791325':ref+='〔方法与局限核读使用作者预印本；正式版差异待对照。〕'
 else:
  r=manual[k];entry=dict(r);entry.update(reference_number=i)
  url=r['url'];title=r['title'];authors='、'.join(r['authors'])
  detail=('('+r['issue']+'):'+r['pages']) if r.get('issue') else r['pages']
  ref=f'{authors}. {title}. {r["venue"]}, {r["year"]}, {detail}. [官方来源]({url}).'
  entry['metadata_checks']={'identity':'大学或期刊官方页面','doi':'未获 DOI，不虚构'}
  p=R/'review'/(k+'.md');p.write_text(f'# {title}\n\n{ref}\n\n核读层级：{r["evidence_level"]}。日期：2026-10-23。\n\n{r["finding"]}\n\n适用边界：{r["boundary"]}\n\n下一步：{r["next_check"]}\n')
 locs=[]
 for para in s.split('\n\n'):
  if '{{cite:'+k+'}}' in para:
   before=s[:s.index(para)];headers=re.findall(r'^#{2,3} (.+)$',before,re.M)
   locs.append({'section':headers[-1] if headers else '引言','paragraph':re.sub(r'\{\{cite:.*?\}\}','',para)})
 entry['cited_at']=locs;audit.append(entry);refs.append(f'{i}. {ref}')
 s=s.replace('{{cite:'+k+'}}',f'[〔{i}〕]({url})')
s=s.replace('<!-- REFERENCES -->','## 参考文献\n\n'+'\n\n'.join(refs)+'\n\n---\n\n检索范围、逐项核读层级、全文获取缺口及工具说明见 [综述方法与核读边界](../literature/review/综述方法与核读边界.md) 和 [引文与证据核对表](../literature/review/引文与证据核对表.md)。\n')
(P/'docs/05-文献综述.md').write_text(s.rstrip()+'\n')
(R/'review/citation-ledger.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
t='# 引文与证据核对表\n\n2026-10-23。本表记录 60 项正文引用的实际依据；摘要核读不等于完整正文评价。DOI 注册与题录检查不能代替论点核对。结论可支持范围和待核问题逐项保留。\n\n'
for r in audit:
 k=r.get('doi',r['id']);card='../cards/'+r['id']+'.md' if 'doi' in r else r['id']+'.md'
 t+=f'## [{r["reference_number"]}] {r["title"]}\n\n- 来源：[原文]({r["url"]})；[核读卡片]({card})。\n- 层级：{r["evidence_level"]}。\n- 引用位置：'+ '；'.join(dict.fromkeys(x['section'] for x in r['cited_at']))+f'。\n- 可支持：{r["finding"]}\n- 边界：{r["boundary"]}\n- 需核对：{r["next_check"]}\n'
 if r.get('additional_reading_source'):t+='- 实际阅读定位：'+json.dumps(r['additional_reading_source'],ensure_ascii=False)+'\n'
 t+='\n'
(R/'review/引文与证据核对表.md').write_text(t.rstrip()+'\n')
f=json.loads((R/'data/focus-decisions.json').read_text());f={x['doi']:x for x in f}
for k,r in rr.items():
 x=f.get(k,dict(id=r['id'],doi=k,title=r['title']));isused=k in keys
 x.update(disposition='进入当前问题链' if isused else '保留可查，本轮不展开',evidence_level=r['evidence_level'],note='2026-10-23 用户要求扩大调研并完成综述；当前用途按正文更新，不是全文排除决定。')
 if isused:
  a=next(a for a in audit if a.get('doi')==k);secs=list(dict.fromkeys(y['section'] for y in a['cited_at']));x.update(question='；'.join(secs),specific_use=r['role'])
 f[k]=x
(R/'data/focus-decisions.json').write_text(json.dumps(list(f.values()),ensure_ascii=False,indent=2))
with (R/'data/当前问题用途.csv').open('w',encoding='utf-8-sig',newline='') as out:
 w=csv.DictWriter(out,fieldnames=['id','doi','title','disposition','question','specific_use','evidence_level','note'],extrasaction='ignore',lineterminator='\n');w.writeheader();w.writerows(f.values())
print(json.dumps({'review_citations':len(keys),'doi_references':len(keys)-len(manual),'official_page_references':len(manual),'chinese_characters_without_bibliography':len(re.findall('[\u4e00-\u9fff]',source.read_text()))},ensure_ascii=False))
