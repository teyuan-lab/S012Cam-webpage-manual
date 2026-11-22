"""Shared small Markdown parser for the S012Cam manual sources."""
import re,html

def inline(s):
 s=html.escape(s.replace('⚠','△'))
 s=re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',s)
 s=re.sub(r'(https://[^\s<>]+)',r'<a href="\1">\1</a>',s)
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
  yield 'caption' if re.match(r'^(Fig\. \d+\.|Figure \d+\.|圖 \d+：)',s) else 'body',' '.join(para)

