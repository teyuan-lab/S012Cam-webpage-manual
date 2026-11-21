"""Build the bilingual S012Cam PDFs and HTML from the reviewed Markdown sources."""
from pathlib import Path
import re,html,hashlib
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Image,Table,TableStyle,PageBreak,KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor,white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT
ROOT=Path(__file__).resolve().parent
# Use an installed font; the final PDF embeds the glyphs it uses.
FONT=Path('/System/Library/Fonts/Supplemental/Arial Unicode.ttf')
pdfmetrics.registerFont(TTFont('Manual',str(FONT)))
pdfmetrics.registerFontFamily('Manual',normal='Manual',bold='Manual',italic='Manual',boldItalic='Manual')
INK=HexColor('#182234');BLUE=HexColor('#165faf');MUTED=HexColor('#52647b');LINE=HexColor('#d9e1eb')
styles={
 'body':ParagraphStyle('body',fontName='Manual',fontSize=10,leading=15,spaceAfter=8,textColor=INK,wordWrap='CJK'),
 'title':ParagraphStyle('title',fontName='Manual',fontSize=26,leading=33,spaceAfter=14,textColor=INK,keepWithNext=True),
 'h2':ParagraphStyle('h2',fontName='Manual',fontSize=17,leading=23,spaceBefore=16,spaceAfter=9,textColor=BLUE,keepWithNext=True,wordWrap='CJK'),
 'h3':ParagraphStyle('h3',fontName='Manual',fontSize=12,leading=18,spaceBefore=10,spaceAfter=6,textColor=BLUE,keepWithNext=True,wordWrap='CJK'),
 'cell':ParagraphStyle('cell',fontName='Manual',fontSize=9,leading=13,textColor=INK,wordWrap='CJK'),
 'caption':ParagraphStyle('caption',fontName='Manual',fontSize=9,leading=14,spaceAfter=12,textColor=MUTED,wordWrap='CJK')}
def inline(s):
 s=html.escape(s.replace('⚠','△'))
 s=re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',s)
 s=re.sub(r'`([^`]+)`',r'<font color="#165faf">\1</font>',s)
 return s

def blocks(text):
 lines=text.splitlines();i=0
 while i<len(lines):
  s=lines[i].strip()
  if not s:i+=1;continue
  if s.startswith('|'):
   rows=[]
   while i<len(lines) and lines[i].strip().startswith('|'):
    line=lines[i].strip()
    if not re.match(r'^\|\s*[-:]+',line):rows.append([c.strip() for c in line.strip('|').split('|')])
    i+=1
   yield 'table',rows;continue
  if s.startswith('#'):
   a,b=s.split(' ',1);yield 'title' if len(a)==1 else 'h2' if len(a)==2 else 'h3',b;i+=1;continue
  if s.startswith('!['):
   m=re.match(r'!\[(.*?)\]\((.*?)\)',s);yield 'image',(m.group(1),m.group(2));i+=1;continue
  if s.startswith('- ') or re.match(r'^\d+\. ',s):yield 'body',s;i+=1;continue
  para=[s];i+=1
  while i<len(lines) and lines[i].strip() and not re.match(r'^(#|\||!\[|- |\d+\. )',lines[i].strip()):
   para.append(lines[i].strip());i+=1
  yield 'caption' if s.startswith(('Figure 1.','圖 1：')) else 'body',' '.join(para)

def footer(c,doc):
 c.setStrokeColor(LINE);c.line(48,43,547,43)
 c.setFont('Manual',8);c.setFillColor(MUTED);c.drawString(48,29,'S012Cam 2.0 · 2026-11-21');c.drawRightString(547,29,str(doc.page))

for lang in ('en','zh'):
 source=ROOT/f'S012Cam-user-manual-{lang}.md';text=source.read_text()
 for style in styles.values():style.wordWrap='CJK' if lang=='zh' else None
 pdf=ROOT.parent/'assets'/f's012cam-user-manual-{lang}.pdf'
 story=[];web=[]
 for kind,data in blocks(text):
  if kind in ('title','h2','h3'):
   if kind=='h2' and data.startswith(('6.','7.','8.')):story.append(PageBreak())
   if kind=='title':story.append(Image(str(ROOT.parent/'assets/icon.png'),width=52,height=52,hAlign='LEFT'));story.append(Spacer(1,10))
   story.append(Paragraph(inline(data),styles[kind]));web.append(f'<{dict(title="h1",h2="h2",h3="h3")[kind]}>{inline(data)}</{dict(title="h1",h2="h2",h3="h3")[kind]}>')
  elif kind=='image':
   alt,path=data;image=Image(str(ROOT/path));image.drawWidth=499;image.drawHeight=499*1206/2622;story.append(image);story.append(Spacer(1,7));web.append(f'<figure><a href="{path}"><img src="{path}" alt="{alt}"></a></figure>')
  elif kind=='table':
   n=len(data[0]);first=data[0][0]
   if first in ('No.','編號'):widths=[38,112,349]
   elif n==3:widths=[137,57,305]
   else:widths=[152,347]
   camera=first in ('No.','編號')
   cellstyle=ParagraphStyle('camera-cell',parent=styles['cell'],fontSize=8.5,leading=11.5) if camera else styles['cell']
   rows=[[Paragraph(inline(c),cellstyle) for c in row] for row in data]
   t=Table(rows,colWidths=widths,repeatRows=1,hAlign='LEFT')
   t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#eaf0f8')),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,0),.7,LINE),('LINEBELOW',(0,1),(-1,-1),.35,LINE),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
   if camera:t.setStyle(TableStyle([('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
   story.extend([KeepTogether([t,Spacer(1,12)]) if len(data)<=5 else t,Spacer(1,12)])
   web.append('<table><thead><tr>'+''.join('<th>'+inline(c)+'</th>' for c in data[0])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+inline(c)+'</td>' for c in row)+'</tr>' for row in data[1:])+'</tbody></table>')
  else:
   story.append(Paragraph(inline(data),styles[kind]));web.append('<p>'+inline(data)+'</p>')
 doc=SimpleDocTemplate(str(pdf),pagesize=(595.28,841.89),leftMargin=48,rightMargin=48,topMargin=40,bottomMargin=59,title='S012Cam User Manual - '+lang+' - 2.0',author='Department of Optics and Photonics, National Central University, Taiwan')
 doc.build(story,onFirstPage=footer,onLaterPages=footer)
 other='zh' if lang=='en' else 'en';label='繁體中文' if lang=='en' else 'English'
 page='<!doctype html><html lang="'+('en' if lang=='en' else 'zh-Hant')+'"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>S012Cam 2.0 User Manual</title><style>body{max-width:1000px;margin:24px auto;padding:0 20px;font:17px/1.75 system-ui;color:#182234}h1,h2,h3{line-height:1.3}h2{margin-top:2em;color:#165faf}a{color:#165faf}img{width:100%;height:auto}figure{margin:20px 0}table{width:100%;border-collapse:collapse;font-size:15px}th,td{padding:10px 8px;text-align:left;vertical-align:top;border-bottom:1px solid #d9e1eb}th{background:#eaf0f8}td{overflow-wrap:anywhere}nav{display:flex;flex-wrap:wrap;gap:20px}@media print{nav{display:none}}</style><nav><a href="../'+('' if lang=='en' else 'zh/')+'">'+('Website' if lang=='en' else '網站')+'</a><a href="S012Cam-user-manual-'+other+'.html">'+label+'</a><a href="../assets/s012cam-user-manual-'+lang+'.pdf">PDF</a></nav>'+''.join(web)+'</html>'
 (ROOT/f'S012Cam-user-manual-{lang}.html').write_text(page)
 print(pdf)
