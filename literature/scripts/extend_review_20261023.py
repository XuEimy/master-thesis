#!/usr/bin/env python3
"""Apply explicitly reviewed additions and reading upgrades, not automatic screening."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
rows='''10.1145/1735223.1735243|记忆系统设计：捕捉目标|作者机构摘要核读|Sellen 与 Whittaker 主张从人类记忆的心理基础出发设计生活日志，而非追求捕捉一切。|本轮仅直接读到机构摘要；五类活动的具体界定不能冒充本篇正文核读。|取得原文，核对情境特定捕捉和不同记忆活动的定义。
10.1002/acp.4033|认知心理学与实践：智能日记|摘要、方法与结果部分核读|研究一让 12 名新用户使用 Day One 两周，研究二访谈 4 名长期用户；研究一的图片、文字、声音和地点使用存在差异，记录与不记录同类日常事件可发生在同一个人身上。|研究一要求每天约 15 分钟，不能当作自然持续使用；功能选择原因部分未系统分析，主观记忆感受不是客观测验。|继续核读长期用户结果及全部讨论；检验习惯变化和实际回看行为。
10.1108/oir-03-2018-0108|信息与设计：自动及手动照片回看|出版社结构化摘要核读|两组用户记录五天，在第 8、50、200 天访谈；自动生活日志照片组的解释立场随时间改变更明显，晚期更倾向重新理解过去。|解释层次变化不是记忆准确性或回忆数量增加；人数、分组控制和流失仍待全文核对。|获取正文，检查样本、分组与图像解释的编码。首发 2019，卷期 2020。
10.1016/j.concog.2025.103983|认知心理学：线索格式与内容比较|摘要与总讨论核读|实验一 101 人使用 208 个不同格式和内容的线索；研究二 106 人评价线索。提取率与线索对任务的贴合、具体性等有关，容易提取的回忆未必更具有自传意义。|不能从统一实验线索推出某个人的照片或视频必然更差；格式、内容和任务映射需要分开。|核读具体线索、分配和统计；公开材料可帮助后续操作化。卷期为 2026，不能按 DOI 后缀写 2025。
10.1093/geronb/gbaf093|认知老化：真实生活照片训练|摘要与结论片段核读|老年人随机分为生活照片自传体记忆训练、一般场景图片训练、词汇控制；在家每周五天持续四至五周，自传体训练对生活事件时间顺序任务的迁移更好。|有训练与反馈，且主要测时间顺序；不能推广为被动记录或偶发推送能普遍改善日常回忆。研究未预注册。|核读样本量、流失、基线及交互效应，区分训练效果与相机本身效果。
10.1017/mem.2026.10057|媒介研究：算法回忆的承诺|摘要与部分正文核读|研究记忆产品的宣传话语与算法化想象，讨论自动整理和再呈现怎样预先规定何种数据被当作可回忆内容。|产品话语分析不证明实际用户获益或受损；不能把平台声称的增强当实验结果。|继续核读样本产品、话语材料选择和分析程序。已核实在线发表 2026-10-12。
10.1177/0956797614542274|社会心理学：日常记录的未来价值|作者机构论文摘要核读|四项研究显示人们可能低估未来重新发现日常经历时的兴趣与愉悦，普通经历尤为明显。|因变量主要为兴趣、愉悦和记录选择；不是回忆细节准确率，也不能据此要求记录所有日常活动。|核读各研究材料、时间间隔、效应与开放数据；当前未完成数据复核。
10.1016/j.actpsy.2025.104929|认知心理学：生活日志视角|出版社摘要核读|32 名成人的受控研究中，第一与第三人称生活日志的记忆表现没有出现预期视角差异；生活日志相对无记录条件改善主观记忆和视觉信息表现，非视觉信息未见同样改善。|未检出差异不是两视角普遍等效；小样本受控活动不能直接确定日常设备视角。|核读任务、回看过程、分配和效应区间，检验视觉与非视觉测验差异。'''
p=R/'data/curation-decisions-additional.json';old={x['doi']:x for x in json.loads(p.read_text())}
for line in rows.splitlines():
 d=dict(zip(['doi','role','evidence_level','finding','boundary','next_check'],line.split('|')));old[d['doi']]=d
old['10.1145/3772318.3791325'].update(evidence_level='摘要及作者预印本方法、局限核读',finding='24 人先使用 Krea AI，再使用 Memory Printer，以不同回忆完成两项任务；质性分析讨论分层生成、实体操作与缓慢制作中的控制感及创造性体验。',boundary='固定顺序、不同回忆和多项交互变化同时存在，不能隔离慢速或实体操作的因果效果。23 人为 22–31 岁；未深入检验虚假记忆问题。',next_check='对照会议正式版与预印本；核读完整结果和编码。不得据此宣称准确记忆改善。')
old['10.1186/s41235-025-00627-4'].update(evidence_level='摘要、方法、部分结果与讨论核读',boundary='思维出声编码区分内部与外部检索，但内部检索合并了无辅助和材料提示后的回忆，不能隔离提示的净效应；非全部细节有独立真值。')
p.write_text(json.dumps(list(old.values()),ensure_ascii=False,indent=2))
p=R/'scripts/build_curated.py';s=p.read_text();s=s.replace('跨学科模型：数字自传体记忆|摘要核读','跨学科模型：数字自传体记忆|摘要及编码、整理框架部分核读').replace('原文下载返回 HTML，网页直取 403；继续取得正文比较本论文拟议映射的增量。','作者机构 PDF 已获取并部分核读；继续通读模型与本论文拟议映射的差异。');p.write_text(s)
p=R/'data/review-access.json';a=json.loads(p.read_text())
loc={'amedia-2024':'摘要及编码、整理概念；文本 80–135、320–385；非完整正文', 'memory-printer-2026-preprint':'方法 355–440、讨论片段 690–735、局限 850–895；作者预印本，非完整正文', 'mediated-remembering-2025':'方法 158–185、220–280，结果 339–390，讨论 560–610；非完整正文'}
for x in a:
 if x['name'] in loc:x.update(status='downloaded_partially_read',locator=loc[x['name']])
 if x['name']=='photobox-2014':x['note']='直接下载 403；网页索引摘要及方法片段可读，不代表本机已取得 PDF'
p.write_text(json.dumps(a,ensure_ascii=False,indent=2))
manual=[dict(id='CN2025-wu-song',title='日常痕迹的算法唤醒：年度报告作为代具记忆',authors=['吴璟薇','宋思静'],year=2025,venue='新闻与写作',issue='8',pages='95–106',url='https://xwxz.cbpt.cnki.net/portal/journal/portal/client/paper/f842de432b0bd59e5d449030f09508a6',evidence_level='期刊官方页面摘要核读',finding='以界面漫游与深度访谈讨论年度报告的日常痕迹激活、平台分类与用户再解释。',boundary='摘要未给样本与完整编码；不是回忆准确性实验。',next_check='需登录获取正文，检查访谈样本、产品、算法机制证据和分析范围。'),dict(id='CN2025-gao',title='数字时代的媒介怀旧研究：以CCD相机的使用为例',authors=['高涔朝'],year=2025,venue='清华大学硕士学位论文',pages='72 页',url='https://newetds.lib.tsinghua.edu.cn/qh/paper/summary?dbCode=ETDQH&sysId=297831',evidence_level='大学学位论文库摘要核读',finding='从实践理论讨论手动操作、主动观察和照片跨媒介导出在记录及怀旧过程中的作用。',boundary='不能把怀旧风格或行动间隔当作记忆准确性提升；样本及具体方法待正文核对。',next_check='需获取正文，核实实践材料、样本、访谈及设备风格论证。')]
(R/'review/manual-sources.json').write_text(json.dumps(manual,ensure_ascii=False,indent=2))
print('Applied 8 DOI additions, 3 reading upgrades and 2 Chinese official-source abstracts')
