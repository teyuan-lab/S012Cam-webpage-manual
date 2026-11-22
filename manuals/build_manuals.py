"""Build the bilingual S012Cam PDF downloads from the reviewed Markdown sources."""
from pathlib import Path
import re,html,hashlib
from reportlab import rl_config
rl_config.useA85 = 0
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
from markdown_render import inline, blocks

def footer(c,doc):
 c.setStrokeColor(LINE);c.line(48,43,547,43)
 c.setFont('Manual',8);c.setFillColor(MUTED);c.drawString(48,29,'S012Cam 2.0 · 2026-11-22');c.drawRightString(547,29,str(doc.page))

for lang in ('en','zh'):
 source=ROOT/f'S012Cam-user-manual-{lang}.md';text=source.read_text()
 for style in styles.values():style.wordWrap='CJK' if lang=='zh' else None
 pdf=ROOT.parent/'assets'/f's012cam-user-manual-{lang}.pdf'
 story=[]
 for kind,data in blocks(text):
  if kind in ('title','h2','h3'):
   if kind=='h2' and data.startswith(('6.','7.','8.','9.','10.')):story.append(PageBreak())
   if kind=='h3' and data.startswith(('Example 1.','Example 2.','Example 3.','範例 1：','範例 2：','範例 3：','Without a Rotator:','沒有 Rotator：')):story.append(PageBreak())
   if kind=='title':story.append(Image(str(ROOT.parent/'assets/icon.png'),width=52,height=52,hAlign='LEFT'));story.append(Spacer(1,10))
   story.append(Paragraph(inline(data),styles[kind]))
  elif kind=='image':
   alt,path=data;image=Image(str(ROOT/path));ratio=image.imageHeight/image.imageWidth;image.drawWidth=min(499,480/ratio);image.drawHeight=image.drawWidth*ratio;image.keepWithNext=True;story.append(image);story.append(Spacer(1,7))
  elif kind=='table':
   n=len(data[0]);first=data[0][0]
   if first in ('No.','編號'):widths=[38,112,349]
   elif n==3:widths=[160,115,224] if first in ('Setup','手機與偏振片配置') else [137,57,305]
   else:widths=[152,347]
   camera=first in ('No.','編號')
   cellstyle=ParagraphStyle('camera-cell',parent=styles['cell'],fontSize=8.5,leading=11.5) if camera else styles['cell']
   rows=[[Paragraph(inline(c),cellstyle) for c in row] for row in data]
   t=Table(rows,colWidths=widths,repeatRows=1,hAlign='LEFT')
   t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#eaf0f8')),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,0),.7,LINE),('LINEBELOW',(0,1),(-1,-1),.35,LINE),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
   if camera:t.setStyle(TableStyle([('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
   story.extend([KeepTogether([t,Spacer(1,12)]) if len(data)<=5 else t,Spacer(1,12)])
  else:
   paragraph=Paragraph(inline(data),styles[kind]);story.append(KeepTogether([paragraph]) if data.startswith(('Hand rotation makes','手動轉動時')) else paragraph)
 doc=SimpleDocTemplate(str(pdf),pagesize=(595.28,841.89),leftMargin=48,rightMargin=48,topMargin=40,bottomMargin=59,title='S012Cam User Manual - '+lang+' - 2.0',author='Department of Optics and Photonics, National Central University, Taiwan')
 doc.build(story,onFirstPage=footer,onLaterPages=footer)
 print(pdf)
