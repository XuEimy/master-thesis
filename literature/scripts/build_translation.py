"""将本地中文译稿生成可检索 PDF 与便于阅读的 HTML；需要 reportlab。"""
import html, re
from pathlib import Path
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether
from reportlab.lib.units import mm
ROOT=Path(__file__).resolve().parents[1]
font=Path('/System/Library/Fonts/Supplemental/Arial Unicode.ttf')
pdfmetrics.registerFont(TTFont('Unicode',str(font)))

def inline(s):
    s=html.escape(s)
    s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',lambda m:f'<a href="{m[2]}">{m[1]}</a>',s)
    s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s)
    s=re.sub(r'\*([^*]+)\*',r'<i>\1</i>',s)
    return s.replace('`','')

for src in sorted((ROOT/'translations').glob('*-中文译稿.md')):
    blocks=src.read_text().split('\n\n');flow=[];web=[]
    for block in blocks:
        block=block.strip()
        if not block:continue
        m=re.match(r'^(#{1,4}) (.+)',block)
        if m:
            level=len(m[1]);text=m[2];size={1:20,2:15,3:12.5,4:11.5}[level]
            style=ParagraphStyle('h',fontName='Unicode',fontSize=size,leading=size*1.5,textColor=colors.HexColor('#163747'),spaceBefore=14,spaceAfter=7,wordWrap='CJK',keepWithNext=True)
            flow.append(Paragraph(inline(text),style));web.append(f'<h{level}>{inline(text)}</h{level}>');continue
        style=ParagraphStyle('p',fontName='Unicode',fontSize=10.5,leading=18,spaceAfter=9,wordWrap='CJK',alignment=TA_LEFT)
        if block.startswith('> '):
            style.leftIndent=12;style.textColor=colors.HexColor('#4a5a60');block=block[2:]
        if block.startswith('- '):
            for line in block.splitlines():
                flow.append(Paragraph('• '+inline(line.removeprefix('- ')),style))
            web.append('<ul>'+''.join('<li>'+inline(x.removeprefix('- '))+'</li>' for x in block.splitlines())+'</ul>')
        else:
            text=' '.join(block.splitlines());flow.append(Paragraph(inline(text),style));web.append('<p>'+inline(text)+'</p>')
    dest=src.with_suffix('.pdf')
    def page(c,d):
        c.setFont('Unicode',8);c.setFillColor(colors.HexColor('#697780'));c.drawString(20*mm,14*mm,'AMEDIA 模型 · 中文译稿 · 原作 CC BY 4.0');c.drawRightString(190*mm,14*mm,str(d.page))
    SimpleDocTemplate(str(dest),pagesize=(210*mm,297*mm),rightMargin=20*mm,leftMargin=20*mm,topMargin=19*mm,bottomMargin=23*mm,title='理解数字时代的自传体记忆：AMEDIA 模型（中文译稿）',author='原作 Hutmacher, Appel & Schwan；AI 中文翻译').build(flow,onFirstPage=page,onLaterPages=page)
    doc='<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AMEDIA 模型 · 中文译稿</title><style>body{max-width:850px;margin:48px auto;padding:0 24px;font:18px/1.9 system-ui,sans-serif;color:#20323c;background:#fafaf7}h1{font-size:2em;line-height:1.5}h2{border-top:1px solid #ccd5d7;padding-top:30px;margin-top:42px;font-size:1.5em}h3{font-size:1.25em;margin-top:32px}h4{font-size:1.1em}a{color:#166c89}p{margin:0 0 1em}li{margin:8px 0}@media print{body{max-width:none;background:white;font-size:11pt}}</style><main>'+''.join(web)+'</main></html>'
    src.with_suffix('.html').write_text(doc)
    print(dest)
