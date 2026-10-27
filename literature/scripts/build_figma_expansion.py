"""Build editable Figma text from current project sources only; no old-canvas input."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / 'docs'
SOURCE_PATHS = [
    'docs/01-选题与研究框架.md',
    'docs/02-导师指导与上下文.md',
    'docs/05-文献综述.md',
    'docs/07-开题研究框架与实施方案.md',
    'literature/review/citation-ledger.json',
    'literature/review/综述方法与核读边界.md',
]


def plain(text):
    text = re.sub(r'\[〔(\d+)〕\]\([^\n)]+\)', r'〔\1〕', text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1（\2）', text)
    text = text.replace('**', '').replace('`', '')
    return text.strip()


def blocks(text):
    result = []
    for part in re.split(r'\n\s*\n', text.strip()):
        part = part.strip()
        if not part:
            continue
        if part.startswith('### '):
            result.append({'kind': 'heading', 'text': plain(part[4:])})
        elif part.startswith('|'):
            lines = [x for x in part.splitlines() if not re.match(r'^\|[\s:|\-]+\|$', x)]
            rows = [[plain(c) for c in line.strip('|').split('|')] for line in lines]
            keys = rows[0]
            for row in rows[1:]:
                result.append({'kind': 'heading', 'text': row[0]})
                result.append({'kind': 'body', 'text': '\n'.join(k+'：'+v for k, v in zip(keys[1:], row[1:]))})
        else:
            result.append({'kind': 'body', 'text': plain(re.sub(r'^> ?', '', part, flags=re.M))})
    return result


def sections(md):
    parts = re.split(r'^## (.+)\n', md, flags=re.M)
    return [(parts[i], parts[i+1]) for i in range(1, len(parts), 2)]


review = (DOCS/'05-文献综述.md').read_text()
framework = (DOCS/'07-开题研究框架与实施方案.md').read_text()
ledger = json.loads((ROOT/'literature/review/citation-ledger.json').read_text())
refs = dict(re.findall(r'^(\d+)\. (.+)$', review, re.M))
assert len(ledger) == 60 and len(refs) == 60
boards = []

for title, body in sections(framework):
    prefix = title[0]
    col = 0 if prefix in ('A', 'C') else 2
    boards.append({'key': title.split()[0], 'column': col, 'title': title,
                   'status': '选题与范围｜当前工作基线' if prefix == 'A' else '本研究拟议内容｜候选关系与实施方案，尚待研究验证',
                   'blocks': blocks(body), 'source': 'docs/07-开题研究框架与实施方案.md'})

for title, body in sections(review):
    if title == '参考文献':
        continue
    key = 'B'+title.split()[0]
    boards.append({'key': key, 'column': 1, 'title': 'B｜'+title,
                   'status': '完整文献综述草稿｜沿用本轮正文；〔编号〕对应右侧证据附录',
                   'blocks': blocks(body), 'source': 'docs/05-文献综述.md'})

for start in range(0, len(ledger), 10):
    bs = []
    for row in ledger[start:start+10]:
        n = row['reference_number']
        bs.append({'kind': 'heading', 'text': f'〔{n}〕{row["title"]}'})
        bs.append({'kind': 'source', 'text': plain(refs[str(n)])})
        used_at = list(dict.fromkeys(x['section'] for x in row.get('cited_at', [])))
        for label, value in [
            ('在本轮综述中的作用', row.get('role', '见引用位置')),
            ('实际核读层级', row['evidence_level']),
            ('可支持的判断', row['finding']),
            ('适用边界', row['boundary']),
            ('仍需核对', row['next_check']),
            ('引用位置', '；'.join(used_at)),
        ]:
            if value:
                bs.append({'kind': 'body', 'text': label+'：'+value})
        loc = row.get('additional_reading_source')
        if loc:
            bs.append({'kind': 'source', 'text': '已记录的阅读定位：'+json.dumps(loc, ensure_ascii=False)})
    boards.append({'key': f'E{start//10+1}', 'column': 3,
                   'title': f'E｜逐篇证据 {start+1:02}—{start+10:02}',
                   'status': '仅使用本轮 citation-ledger｜条目不等于独立实验，摘要与正文片段按原状态保留',
                   'blocks': bs, 'source': 'literature/review/citation-ledger.json；docs/05-文献综述.md'})

method = (ROOT/'literature/review/综述方法与核读边界.md').read_text()
for title, body in sections(method):
    if title in ('交付范围', '对结论影响较大的待核问题'):
        boards.append({'key': 'F1' if title == '交付范围' else 'F2', 'column': 2,
                       'title': 'F｜'+title, 'status': '本轮综述的方法与获取边界，原文保留',
                       'blocks': blocks(body), 'source': 'literature/review/综述方法与核读边界.md'})

index = {
    'key': 'INDEX', 'column': -1, 'title': '本轮研究｜完整文字展开稿',
    'status': '2026-10-23｜面向个人回忆唤起的 AI 辅助生活记录与表达设计研究（暂定）',
    'blocks': [
        {'kind': 'body', 'text': '阅读顺序：左侧保留 17 页摘要；本区域从左到右依次为选题与框架、完整文献综述、研究实施方案、逐篇证据附录。各列从上往下阅读。'},
        {'kind': 'heading', 'text': 'A + C｜研究问题与框架如何形成'},
        {'kind': 'body', 'text': '从背景、概念和三个研究问题出发，展开文献如何支持各环节、候选线索、对应规则、AI 与用户分工及尚未确定的关系。'},
        {'kind': 'heading', 'text': 'B｜完整文献综述'},
        {'kind': 'body', 'text': '保留本轮七节综述的连续论证、跨研究比较和边界。表格转为逐项文字，引用编号保持一致。'},
        {'kind': 'heading', 'text': 'D + F｜怎样研究、实现与验证'},
        {'kind': 'body', 'text': '展开四项研究任务，以及用户材料、分析、输入与工程、AI 原型、比较方案、评价和框架修订。具体条件、样本与时长仍待前期研究确定。'},
        {'kind': 'heading', 'text': 'E｜60 项正文引文的可追溯依据'},
        {'kind': 'body', 'text': '逐项保留完整题录、原文链接、实际核读层级、可支持判断、边界、待核问题和引用位置。没有将全部来源标为全文已读。'},
        {'kind': 'body', 'text': '文字层级：文献结果与理论依据／跨研究综合／本研究拟议方案分别说明。旧版仅参照展开程度，本区域不导入旧版资料和研究路线。'},
    ], 'source': 'docs/05-文献综述.md；docs/07-开题研究框架与实施方案.md；literature/review/citation-ledger.json'
}
boards.insert(0, index)
manifest = {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in SOURCE_PATHS}
out = {'date':'2026-10-23', 'fileKey':'R1Z5ryhzvwXJqO6ofxLgA3', 'pageId':'101:2',
       'source_sha256': manifest, 'boards':boards}
(DOCS/'Figma展开稿数据.json').write_text(json.dumps(out, ensure_ascii=False, indent=2)+'\n')
summary = {'board_count':len(boards), 'editable_text_blocks':sum(len(b['blocks'])+3 for b in boards),
           'characters':sum(len(b['title'])+len(b['status'])+sum(len(x['text']) for x in b['blocks']) for b in boards),
           'source_count':len(ledger), 'sections':{str(c):sum(b['column']==c for b in boards) for c in [-1,0,1,2,3]}}
(DOCS/'Figma展开稿构建核对.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2)+'\n')
print(json.dumps(summary, ensure_ascii=False))
