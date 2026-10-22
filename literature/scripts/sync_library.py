#!/usr/bin/env python3
"""Render indexes/queues from curated decisions; retain existing access evidence."""
import csv,json,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
rr=[json.loads(x) for x in (R/'data/curated-records.jsonl').open()]
queue_path=R/'data/fulltext-queue.json';old={x['doi']:x for x in json.loads(queue_path.read_text())} if queue_path.exists() else {}
queue=[];ris=[]
for r in rr:
 q=old.get(r['doi'],{'status':'摘要或局部正文已核读，尚未逐一尝试完整原文获取','action':'先检查开放版本，必要时机构登录'})
 q.update(id=r['id'],doi=r['doi'],title=r['title'],url='https://doi.org/'+r['doi'],question=r['next_check'])
 if r['evidence_level']=='正文核读':q.update(status='正文已核读，附录／原始数据等尚未复核',action='按文献卡及 verification-notes.json 进行后续核实')
 if r['doi']=='10.1098/rstb.2019.0693':q.update(status='Europe PMC 全文 XML 两次 HTTP 500；摘要可读',action='尝试 PMC 网页或出版社；不能据 500 判为付费墙')
 if r['doi'] in ['10.1186/s41235-025-00627-4','10.1017/mem.2025.3']:q.update(status='已确认开放获取；摘要或局部正文已读',action='继续完整正文核读，无需优先等待登录')
 queue.append(q)
 typ={'proceedings-article':'CPAPER','book-chapter':'CHAP','book':'BOOK','dissertation':'THES','journal-article':'JOUR'}.get(r.get('publication_type'),'GEN')
 ris+=['TY  - '+typ,'TI  - '+r['title']]+['AU  - '+a for a in r['authors']]+['JO  - '+v for v in r['venue']]
 dt=r['dates'].get('published-print') or r['dates'].get('published-online') or r['dates'].get('published')
 if dt:ris+=['PY  - '+str(dt[0][0])]
 ris+=['DO  - '+r['doi'],'UR  - '+q['url'],'N1  - '+r['evidence_level']+'；首发与卷期日期及待核问题详见文献卡','ER  - ','']
queue_path.write_text(json.dumps(queue,ensure_ascii=False,indent=2));(R/'data/已核读文献.ris').write_text('\n'.join(ris))
s='# 原文获取与核读队列\n\n更新：2026-10-23。资料暂不可读仍保留。登录限制、网络失败、未尝试、获取成功及正文核读分别记录。用户计划次日协助登录；开放来源继续独立推进。\n\n'
for q in queue:
 s+=f"### {q['title']}\n\n- [原文入口]({q['url']})；[文献卡](cards/{q['id']}.md)。\n- 状态：{q['status']}。\n- 下一步：{q['action']}。\n- 核读问题：{q['question']}\n\n"
s+='## 尚未进入文献卡的来源\n\n相关的元数据节点、未筛选命中及引文候选仍在总库和检索日志内，不因缺原文被删除。此队列不是所有检索命中都已经尝试获取的声明。\n'
(R/'待获取原文.md').write_text(s)
# Readable complete index of curated nodes, including evidence level and role.
s='# 逐篇阅读索引\n\n这里只列已作内容核读的节点；完整未筛选命中保留在总库。日期的网络首发与卷期差异见卡片。\n\n| 文献 | 作用 | 核读层级 |\n|---|---|---|\n'
for r in rr:s+=f"| [{r['title']}](../cards/{r['id']}.md) | {r['role']} | {r['evidence_level']} |\n"
(R/'chains/09-逐篇阅读索引.md').write_text(s)
refs=[];curated_dois={r['doi'] for r in rr}
for p in (R/'sources/crossref').glob('*.json'):
 m=json.loads(p.read_text())['message']
 if m['DOI'].lower() not in curated_dois:continue
 for ref in m.get('reference',[]):refs.append(dict(source_doi=m['DOI'].lower(),target_doi=ref.get('DOI','').lower(),reference=ref,relation='publisher_reference_metadata',evidence=str(p.relative_to(R)),note='出版社参考文献元数据，未核对具体引用语境'))
(R/'data/publisher-reference-edges.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in refs))
counts={'curated_reports':len(rr),'body_read':sum(r['evidence_level']=='正文核读' for r in rr),'publisher_reference_entries':len(refs),'synthesis_edges':sum(1 for x in (R/'data/relation-edges.jsonl').open()),'date':'2026-10-23','note':'报告／文献节点数，不是独立研究数；正文核读不等于附录与数据复核'}
focus_path=R/'data/focus-decisions.json'
if focus_path.exists():
 focus=json.loads(focus_path.read_text())
 counts['focused_nodes']=sum(x.get('disposition')=='进入当前问题链' for x in focus)
 counts['focus_scope']='三个研究问题的文献串联；订阅库内部检索与未获取全文单列，不声称全球零遗漏'
(R/'data/library-state.json').write_text(json.dumps(counts,ensure_ascii=False,indent=2));print(json.dumps(counts,ensure_ascii=False))
