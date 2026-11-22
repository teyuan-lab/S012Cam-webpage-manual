"""Shared bilingual shell for the static S012Cam website."""
from pathlib import PurePosixPath,Path
import posixpath,html,hashlib,json,re
ROOT=Path(__file__).resolve().parent
ORIGIN='https://teyuan-lab.github.io/S012Cam-webpage-manual/'
PAGES=['polarization','app','rotator','manual','buy','support']
LABELS={'en':['Polarization','App','Rotator','Manual','Buy','Support'],'zh':['偏振簡介','App','Rotator','使用手冊','購買','支援']}

def local(lang,name):return ('zh/' if lang=='zh' else '')+('index.html' if name=='home' else name+'.html')
def rel(current,target):return posixpath.relpath(target,posixpath.dirname(current) or '.')
def canonical(path):return ORIGIN+(path[:-10] if path.endswith('index.html') else path)
def asset(current,name):return rel(current,'assets/'+name)
def render(path,lang,title,description,body,active='',alternate=None,sidebar='',home=False):
 other='zh' if lang=='en' else 'en';alt=alternate or local(other,active or 'home');h=hashlib.sha256((ROOT/'style.css').read_bytes()).hexdigest()[:12]
 def version_script(match):
  source=(ROOT/posixpath.dirname(path)/match[2]).resolve()
  version=hashlib.sha256(source.read_bytes()).hexdigest()[:12]
  return match[1]+match[2]+'?v='+version+match[3]
 body=re.sub(r'(<script\b[^>]*\bsrc=")([^"?]+\.js)(")',version_script,body)
 j=hashlib.sha256((ROOT/'language.js').read_bytes()).hexdigest()[:12]
 nav=''.join(f'<a href="{rel(path,local(lang,k))}"'+(' aria-current="page"' if k==active else '')+'>'+label+'</a>' for k,label in zip(PAGES,LABELS[lang]))
 privacy=rel(path,local(lang,'privacy'));homeurl=rel(path,local(lang,'home'))
 label='English' if lang=='zh' else '繁體中文';skip='跳至主要內容' if lang=='zh' else 'Skip to content'
 icon=asset(path,'icon.png');credit='國立中央大學光電科學與工程學系' if lang=='zh' else 'Department of Optics and Photonics, National Central University, Taiwan'
 footerlabel='隱私權政策' if lang=='zh' else 'Privacy policy'
 crumb='' if home else f'<div class="breadcrumb"><a href="{homeurl}">'+('首頁' if lang=='zh' else 'Home')+'</a><span>/</span><span>'+html.escape(title)+'</span></div>'
 inner=crumb+body
 if sidebar:inner='<div class="manual-layout">'+sidebar+'<article class="manual-article">'+inner+'</article></div>'
 routes={'how':rel(path,local(lang,'polarization')),'app':rel(path,local(lang,'app')),'results':rel(path,local(lang,'app'))+'#results','data':rel(path,local(lang,'app'))+'#compatibility','hardware':rel(path,local(lang,'rotator')),'manual':rel(path,local(lang,'manual')),'support':rel(path,local(lang,'support')),'faq':rel(path,local(lang,'support')),'fixed-camera':rel(path,f'manuals/{lang}/fixed.html'),'measure':rel(path,f'manuals/{lang}/gyro.html'),'camera':rel(path,f'manuals/{lang}/camera.html')}
 legacy='<script id="legacy-routes" type="application/json">'+json.dumps(routes)+'</script>' if home else ''
 return f'''<!doctype html>
<html lang="{'zh-Hant' if lang=='zh' else 'en'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} | S012Cam</title><meta name="description" content="{html.escape(description,quote=True)}">
<link rel="canonical" href="{canonical(path)}"><link rel="alternate" hreflang="{'zh-Hant' if lang=='zh' else 'en'}" href="{canonical(path)}"><link rel="alternate" hreflang="{'zh-Hant' if other=='zh' else 'en'}" href="{canonical(alt)}">
<meta property="og:title" content="{html.escape(title)} | S012Cam"><meta property="og:description" content="{html.escape(description,quote=True)}"><meta property="og:image" content="{ORIGIN}assets/icon.png"><meta property="og:url" content="{canonical(path)}">
<link rel="icon" href="{asset(path,'favicon.png')}?v=s012cam2-current"><link rel="apple-touch-icon" href="{asset(path,'apple-touch-icon.png')}?v=s012cam2-current"><link rel="stylesheet" href="{rel(path,'style.css')}?v={h}"><script src="{rel(path,'language.js')}?v={j}" defer></script></head>
<body><a class="skip" href="#content">{skip}</a><header class="bar"><div class="bar-inner"><a class="brand" href="{homeurl}"><img src="{icon}?v=s012cam2-current" width="32" height="32" alt="">S012Cam</a><nav aria-label="{'主要導覽' if lang=='zh' else 'Main navigation'}">{nav}</nav><a class="language" data-language href="{rel(path,alt)}" lang="{'zh-Hant' if other=='zh' else 'en'}" hreflang="{'zh-Hant' if other=='zh' else 'en'}">{label}</a></div></header>
<main id="content">{inner}</main><footer><div class="footer-inner"><span>© 2026 Te-yuan Chung · {credit}</span><div><a href="{rel(path,local(lang,'support'))}">{'支援' if lang=='zh' else 'Support'}</a><a href="{privacy}">{footerlabel}</a></div></div></footer>{legacy}</body></html>'''
