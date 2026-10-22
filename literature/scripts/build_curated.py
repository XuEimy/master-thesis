#!/usr/bin/env python3
"""Build a curated, evidence-labelled layer separate from unscreened search hits.
Descriptions below are human/assistant reading decisions, not automatic eligibility.
"""
import csv,hashlib,html,json,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def clean(s):return re.sub(r'\s+',' ',re.sub('<[^>]+>',' ',html.unescape(s or ''))).strip()
with (R/'data/records.jsonl').open() as f: pool={r['doi']:r for r in map(json.loads,f) if r.get('doi')}
meta={}
for p in (R/'sources/crossref').glob('*.json'):
 m=json.loads(p.read_text())['message'];meta[m['DOI'].lower()]=(m,str(p.relative_to(R)))
# DataCite preprints use their own registration source; do not claim Crossref verification.
for p in (R/'sources/datacite').glob('*.json'):
 a=json.loads(p.read_text())['data']['attributes'];submitted=next((d['date'][:10] for d in a.get('dates',[]) if d.get('dateType')=='Submitted'),str(a['publicationYear']))
 m={'DOI':a['doi'].lower(),'title':[x['title'] for x in a['titles']], 'author':[{'given':x.get('givenName',''),'family':x.get('familyName') or x['name']} for x in a['creators']], 'container-title':['arXiv（预印本，非已确认同行评审版本）'],'type':'posted-content','published':{'date-parts':[[int(x) for x in submitted.split('-')]]},'abstract':' '.join(x.get('description','') for x in a.get('descriptions',[]) if x.get('descriptionType')=='Abstract')}
 meta[m['DOI']]=(m,str(p.relative_to(R)))
# DOI | role | evidence level | extracted finding | boundary | next check
rows='''10.1037/0033-295x.107.2.261|认知心理学：自我与提取|摘要核读|自传体记忆被解释为自我记忆系统中的暂时建构；当前目标与自传体知识共同约束提取线索。|理论模型不提供传感器清单，也不证明某种 AI 产品有效。|核读知识层级、目标调控及直接与生成性提取的原文定义。
10.1111/j.1745-6916.2006.00017.x|认知心理学：多系统记忆|摘要核读|情景记忆涉及感官、空间表象、语言、情绪、叙事及提取等系统之间的相互作用。|涉及一种心理系统，不等于必须配备对应传感器；声、味等也可能由照片联想出来。|核读各系统的相互作用及其支持证据，区分直接采集与间接唤起。
10.1146/annurev-psych-010419-051101|认知神经科学：事件结构|摘要核读|综述连续体验如何被分成事件，以及事件表征与行动、语言和记忆的关系。|事件分段理论不能直接规定摄像机启动阈值或最优片段时长。|核读自然事件与实验材料的区别，以及边界对跨事件记忆的影响。
10.1177/0963721413475622|人格与叙事：生命故事|摘要核读|叙事身份连接被重构的过去与想象的未来，使经历获得连续性与目的。|人生故事的意义不等同于一次事件细节的准确性；综述也指出因果方向尚需澄清。|区分事件级回忆与生命故事级叙事，核读文化情境与意义建构。
10.1177/27000710241264452|人格与叙事：记忆功能|摘要核读|145 名本科生的两波、间隔八个月研究，比较转折点和低谷记忆中的功能及其稳定性；均值稳定与排序稳定结果不同。|不能把稳定性概括为个人偏好永远固定，也不能据此自动为用户分型。|核对功能编码、稳定性效应、样本流失和事件类型。
10.1177/1470357207084865|媒介研究：摄影实践|摘要及部分正文核读|个人摄影中的记忆、交流与身份功能相互交织；技术变化要放回社会文化使用中理解。|文化分析不提供拍照改善记忆的因果效应；原文中的旧实验需追溯而非二手当作新发现。|作者接受稿已获取；继续核读全文，并追溯与本题有关的原始研究。
10.1177/1461444814532062|媒介研究：记录到回看的实践|摘要核读|通过拍摄、存储、观看、分享四类实践讨论模拟与数字摄影中的变化及延续。|实践类别不自动成为四个独立实验变量；不能仅以新设备推出推断习惯变化。|核读材料来源与分析方式，比较具体人群和使用情境。
10.1177/1750698019829891|分布式认知：摄影与回忆|摘要核读|结合两项质性研究提出 blended memory，强调照片、个人摄影史和其他资源在回忆活动中的相互依赖。|这是理论及质性综合，不能给出单个线索的平均提升幅度。|核读两研究与后续 Cued recall 是否共用样本，建立报告与研究对应。
10.1177/17506980211073093|分布式认知与视觉方法|摘要、方法与结果开头核读|照片诱导访谈将回忆拆分为催发、情绪激活、模拟与叙事、联想、推断及意义建构；方法涉及婚礼参与者 6 人与大学工作人员 15 人两项研究。|样本与情境有限；访谈本身参与建构叙述，不能将全部新增话语都记为准确回忆。|继续核读后续结果与讨论；核对与 Blended memory 的样本重叠。
10.1080/14725860220137345|视觉社会学：照片诱导方法|摘要核读|梳理照片诱导访谈在社会学和人类学中的发展，讨论图像如何带来不同于纯语言访谈的信息、感受与记忆。|访谈能产生丰富叙述，不等于照片使记忆更准确。|核读取材来源、访谈者作用及图片选择方法。
10.1080/1472586x.2011.571888|摄影研究：日常使用|摘要核读|结合多年的经验研究讨论个人摄影作为记忆、关系、自我呈现与自我表达的重叠实践。|这些作用可同时存在，不应强制把每个人分入单一记录动机。|核读各研究的样本和方法，提炼适合访谈的实践问题。
10.1080/17503280.2020.1815123|电影研究：自传体纪录片|摘要核读|以三部自传体纪录片分析家庭档案影像重新语境化及蒙太奇如何参与自我与身份的表达。|作品分析指导取材和表达，不能替代观众回忆效果实验；成片具有作者立场。|核读片段分析与档案、访谈、观察素材的对应方式。
10.1080/17503280.2024.2350603|电影研究：第一人称与归属|摘要核读|围绕 Four Journeys 的作品分析及导演访谈，讨论片中活动、拍摄行为和电影表达三种层次的归属建构。|迁移经历及作者电影的语境不能直接推广到普通日常记录。第一人称电影叙事也不等于头戴摄像机视角。|核读三种层次的重叠、作者立场与可迁移的记录方法。
10.1002/acp.4150|认知心理学：照片与回忆视角|摘要核读|三项研究共 378 人，含本人照片的经历与更多观察者式回忆视角相关。|相关关系不等于拍摄视角的因果效果；观察者视角也不等于记忆变差。|核读自报告照片分类、控制变量及各研究设计。
10.1177/19485506231163012|社会心理学：摄影目标与视角|摘要核读|六项研究共 2113 人，区分捕捉意义与身体体验的目标，并考察第一、第三人称照片的选择、观看与偏好。|目标与视角匹配不能直接代表准确回忆提升，六项研究的操纵须分别检查。|核读各研究因变量，将选择、意义唤起与喜爱程度分开。
10.1080/09658211.2024.2377193|认知心理学：日常回忆验证|摘要核读|9 名本科生佩戴相机记录两天；一周与一月后先回忆，再查看照片并纠正或补充，区分遗漏类型。|样本很小；准确性由参与者自评，不是独立客观真值。两天及十秒间隔是该研究方法，不是本论文要求。|核读计分单元、遗漏分类、上界估计和准确性评分。
10.3389/fpsyg.2025.1574855|感官与情绪：系统综述|摘要核读|综合以自传体记忆激活为手段的情绪诱导研究，比较不同程序对情绪状态的影响。|主要结果是情绪变化，不能据此排名哪种感官最能恢复真实事件细节。|核读纳入人群、感官操作、异质性和偏倚；追溯单篇实验。
10.1080/1047840x.2024.2384125|跨学科模型：数字自传体记忆|摘要核读|AMEDIA 将数字情境中的回忆理解为内部与外部信息反复整合的过程，并把编码与整理纳入解释。|现有综合框架意味着本论文不能仅凭连接记录、整理、回忆就宣称首次创新。|原文下载返回 HTML，网页直取 403；继续取得正文比较本论文拟议映射的增量。
10.1080/09658211.2025.2602077|认知心理学：现实数字资源使用|摘要核读|预注册思维出声研究中，40 名德国参与者在家回忆两个年份的生日，可使用外部资源；较远事件使用资源更多，资源帮助获得新的认识。|外部信息带来的新认识不自动等于被遗忘的真实细节重新出现；需要核对分类标准。|核读生日任务、编码及准确性验证；区分网络首发 2025 与卷期 2026。
10.1017/mem.2024.16|媒介记忆：AI 与人的能动性|摘要及引言片段核读|讨论生成式 AI 如何改变个人与集体过去的表达、对话和重构，以及人在其中的同意与控制。|理论论述及案例不是改善记忆的实验，也不能把个体和集体记忆混为一层。|核读概念定义与案例来源，将相关论点转化为具体表达边界。
10.2196/30517|信息检索：生活日志综述|摘要核读|综述生活日志的数据、检索方法与应用，为寻找图像、声音、位置等输入及处理路径提供入口。|检索准确率与找回记录不等于人发生回忆；作者的记忆增强展望仍需检查直接证据。|核读研究表格，分别提取传感、事件组织、检索及用户评价。
10.3758/s13428-023-02145-x|记忆测量与自然语言处理|摘要核读|使用微调 distilBERT 识别自传体访谈叙述中的内部与外部内容，并在五个数据集中与人工评分比较。|细节分类与人工分数相关，不是验证叙述真实，也不直接验证中文适用性。|核读评分标注、数据划分、预处理及迁移限制。
10.3758/s13428-025-02767-3|记忆测量与大语言模型|摘要核读|使用微调 LLaMA-3 处理过去与未来事件叙述，在三项研究的 284 人材料中与人工内部、外部细节评分对照。|未来想象也能获得细节分，因此细节数量不能单独证明记忆真实；不能直接用通用聊天模型替代。|核读模型训练、外部验证、错误类型、开放实现与语言范围。
10.3724/sp.j.1042.2014.00269|认知心理学：自发回忆|期刊摘要核读|综述没有预先提取意图时自发浮现的个人经历记忆，以及相关功能、特征和解释理论。|系统推送不必然造成自发回忆；看到提醒与主观想起经历需要分别观察。|继续取得中文全文，追溯直接提取与线索启动研究。
'''
additional_path=R/'data/curation-decisions-additional.json'
if additional_path.exists():
 for item in json.loads(additional_path.read_text()):
  rows+='\n'+'|'.join(item[k] for k in ['doi','role','evidence_level','finding','boundary','next_check'])
curated=[]
for line in rows.splitlines():
 if not line.strip():continue
 doi,role,level,finding,boundary,nextcheck=line.split('|');m,path=meta[doi];r=pool.get(doi,{})
 rid=r.get('id') or 'L'+hashlib.sha256(('doi:'+doi).encode()).hexdigest()[:12]
 provider='DataCite' if path.startswith('sources/datacite/') else 'Crossref'
 metadata_url=('https://api.datacite.org/dois/' if provider=='DataCite' else 'https://api.crossref.org/works/')+doi
 authors=[' '.join([a.get('given',''),a.get('family','')]).strip() for a in m.get('author',[])]
 dates={k:m[k].get('date-parts') for k in ['published-online','published-print','published'] if k in m}
 item=dict(id=rid,doi=doi,title=clean(': '.join(m.get('title',[])[:1]+m.get('subtitle',[])[:1])),authors=authors,venue=m.get('container-title',[]),publication_type=m.get('type'),dates=dates,role=role,evidence_level=level,finding=finding,boundary=boundary,next_check=nextcheck,screening='主题相关，保留继续核读；不是最终全文纳入',reviewed_on='2026-10-23',source_metadata=path,metadata_provider=provider,metadata_url=metadata_url,abstract_source=r.get('provenance',[]),abstract_available=bool(r.get('abstract') or m.get('abstract')),fulltext_status=('正文已核读；未核对附录和原始数据' if level=='正文核读' else '见独立获取记录；未完成全文核读'))
 curated.append(item)
 title=item['title'];date_text='；'.join(k+'='+str(v) for k,v in dates.items())
 text=f'''# {title}\n\n- 编号：{rid}\n- 作者：{'；'.join(authors)}\n- 刊物：{'；'.join(item['venue'])}\n- 日期：{date_text}\n- 原文入口：[DOI](https://doi.org/{doi})\n- 研究作用：{role}\n- 核读状态：{level}；2026-10-23\n- 筛选：主题相关，保留继续核读。是否已读正文见核读状态；论文的最终使用范围仍需结合具体问题确定。\n\n## 当前可支持的内容\n\n{finding}\n\n## 适用边界\n\n{boundary}\n\n## 对本论文的用途\n\n作为“{role}”层面的依据或比较对象；具体设计映射仍是综合推论，不能反写成原作者已验证的设计结论。关系见 [文献串联入口](../chains/00-串联入口.md)。\n\n## 下一步核读\n\n{nextcheck}\n\n## 可追溯来源\n\n题录核对：[{provider}]({metadata_url})；本机原始响应 `{path}`。摘要来源与检索轨迹保存在 `data/curated-records.jsonl` 及总库中。下载、摘要阅读和完整正文阅读分别记录，DOI 核对不代表论点已获全文验证。\n'''
 (R/'cards'/f'{rid}.md').write_text(text)
# Preserve manually checked source locators across regeneration.
existing_path=R/'data/curated-records.jsonl'
existing={}
if existing_path.exists():
 with existing_path.open() as f: existing={r['doi']:r for r in map(json.loads,f)}
for r in curated:
 extra=existing.get(r['doi'],{}).get('additional_reading_source')
 if extra:
  r['additional_reading_source']=extra
  p=R/'cards'/(r['id']+'.md')
  with p.open('a') as f:f.write('\n本轮补充核读来源：`'+extra['path']+'`；位置／范围：'+extra['locator']+'。\n')
existing_path.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in curated))
with (R/'data/已核读文献索引.csv').open('w',encoding='utf-8-sig',newline='') as f:
 fields=['id','doi','title','role','evidence_level','finding','boundary','next_check'];w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(curated)
print('curated',len(curated))
