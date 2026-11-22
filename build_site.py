"""Build the bilingual static pages and manual chapters. No hosting or Git actions."""
from pathlib import Path
import re,html,posixpath,sys,struct
from PIL import Image as PILImage
from site_shell import render,local,rel,asset
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'manuals'))
from markdown_render import blocks,inline
CHAPTERS=[
 ('start',{'en':'Start here','zh':'開始使用'},'intro'),
 ('assembly',{'en':'Assembly and calibration','zh':'組裝與校正'},'intro'),
 ('camera',{'en':'Camera controls','zh':'相機控制'},'intro'),
 ('handheld',{'en':'Handheld iPhone','zh':'手持 iPhone'},'setup'),
 ('fixed',{'en':'Tripod or fixed iPhone','zh':'腳架或固定 iPhone'},'setup'),
 ('gyro',{'en':'Gyro mode','zh':'Gyro 模式'},'mode'),
 ('timer',{'en':'Timer mode','zh':'Timer 模式'},'mode'),
 ('alignment',{'en':'Align and calculate','zh':'對齊與計算'},'mode'),
 ('results',{'en':'Read the results','zh':'結果判讀'},'results'),
 ('files',{'en':'Save, share and export','zh':'儲存、分享與匯出'},'results'),
 ('hand-polarizer',{'en':'Hand-held polarizer','zh':'手持偏振片'},'extra'),
 ('troubleshooting',{'en':'Troubleshooting','zh':'常見問題'},'extra')]
GROUPS={'en':{'intro':'Getting started','setup':'How to support the iPhone','mode':'Capture and calculation','results':'Results and data','extra':'More help'},'zh':{'intro':'開始前準備','setup':'選擇操作方式','mode':'拍攝與計算','results':'結果與資料','extra':'補充與問題'}}
TITLES={'en':{'home':'See how light is polarized','polarization':'Polarization basics','app':'The S012Cam app','rotator':'Polarizer Rotator','manual':'User manual','buy':'Buy a Polarizer Rotator','support':'Support','privacy':'Privacy policy'},'zh':{'home':'用 iPhone 看見光的偏振','polarization':'偏振簡介','app':'S012Cam App','rotator':'Polarizer Rotator','manual':'使用手冊','buy':'購買 Polarizer Rotator','support':'使用支援','privacy':'隱私權政策'}}
DESCS={'en':{'home':'Explore light with S012Cam. Learn the app, use the Rotator, read the manual or choose a kit.','polarization':'An illustrated guide to electric fields, Fresnel reflection, Rayleigh scattering, polarizers, sky and LCD experiments, and 18 applications.','app':'Explore what S012Cam does: visualize linear polarization, compare colour channels and keep measurement data.','rotator':'Assemble, calibrate and use the S012Cam Polarizer Rotator.','manual':'Choose handheld or fixed iPhone operation, then Gyro or Timer. Read online or download the PDF.','buy':'Compare the DIY kit and the fully assembled Polarizer Rotator.','support':'Find capture tips, troubleshooting and contact details.','privacy':'How S012Cam keeps photos, measurements and motion data on your iPhone.'},'zh':{'home':'認識 S012Cam、使用 Rotator、閱讀操作手冊或選購套件。','polarization':'從電場方向到反射、散射、偏振片、藍天與 LCD，搭配圖解、動手實驗與 18 個應用。','app':'認識 S012Cam 的用途與功能：看見線偏振、比較不同色彩通道，並保留量測資料。','rotator':'組裝、校正並操作 S012Cam Polarizer Rotator。','manual':'先選手持或固定手機，再選 Gyro 或 Timer。提供網頁教學與 PDF 下載。','buy':'比較 DIY 套件版與完整組裝版 Polarizer Rotator。','support':'查詢拍攝提示、常見問題與聯絡方式。','privacy':'了解 S012Cam 如何將照片、量測與動作資料保留在你的 iPhone。'}}

def assembly_video(lang,path):
 zh=lang=='zh'
 title='Polarizer Rotator 3D 組裝動畫' if zh else 'Polarizer Rotator 3D assembly animation'
 note='播放 3D 動畫查看零件位置與組裝順序，可隨時暫停或拖動進度條。各步驟的操作細節與校正方式見下方圖文說明。' if zh else 'Watch the 3D animation to see the parts and assembly order. Pause or seek at any time. The illustrated instructions below explain each step and calibration.'
 movie='s012cam-rotator-assembly-3d-'+lang+'.mp4'
 poster='s012cam-rotator-assembly-3d-poster-'+lang+'.jpg'
 return '<section class="animation-panel" aria-label="'+title+'"><h2>'+title+'</h2><p>'+note+'</p><video id="assembly-movie" controls playsinline preload="metadata" poster="'+asset(path,poster)+'"><source src="'+asset(path,movie)+'" type="video/mp4">'+('你的瀏覽器無法播放此影片。' if zh else 'Your browser does not support this video.')+'</video></section>'

def capture_visual(lang,path,mode):
 zh=lang=='zh';title=('Gyro：轉動後持穩，自動拍攝' if mode=='gyro' else 'Timer：在間隔結束前轉好角度') if zh else ('Gyro: turn, hold still, capture automatically' if mode=='gyro' else 'Timer: reach each angle before the interval ends')
 labels=([('0°','按快門拍第 1 張'),('45°','轉到 45°，持穩後自動拍第 2 張'),('90°','轉到 90°，持穩後自動拍第 3 張'),('135°','轉到 135°，持穩後自動拍第 4 張')] if mode=='gyro' else [('0°','按快門拍第 1 張'),('45°','間隔結束前轉到 45°，拍第 2 張'),('90°','間隔結束前轉到 90°，拍第 3 張'),('135°','間隔結束前轉到 135°，拍第 4 張')]) if zh else ([('0°','Press the shutter for photo 1'),('45°','Turn to 45°, then hold still for automatic photo 2'),('90°','Turn to 90°, then hold still for automatic photo 3'),('135°','Turn to 135°, then hold still for automatic photo 4')] if mode=='gyro' else [('0°','Press the shutter for photo 1'),('45°','Reach 45° before the interval ends for photo 2'),('90°','Reach 90° before the interval ends for photo 3'),('135°','Reach 135° before the interval ends for photo 4')])
 return '<section class="capture-demo" aria-label="'+title+'"><h2>'+title+'</h2><p>'+('流程示意，可播放或逐步查看。這是操作教學，不是 App 即時畫面；Gyro 不使用固定秒數。' if zh else 'A guided sequence. Play it or select a step. This illustrates the workflow, not a live app screen; Gyro has no fixed capture interval.')+'</p><div class="sequence-art"><img src="'+asset(path,'s012cam-rotator-positions.png')+'" alt="'+('轉盤四個位置與凸紋指針' if zh else 'Four dial positions and the ridge pointer')+'"><div class="sequence-focus" aria-hidden="true"></div></div><div class="sequence-buttons">'+''.join('<button type="button" data-step="'+str(i)+'" aria-pressed="'+('true' if i==0 else 'false')+'">'+a+'</button>' for i,(a,b) in enumerate(labels))+'</div><div class="sequence-labels" aria-live="polite">'+''.join('<p'+(' hidden' if i else '')+'>'+b+'</p>' for i,(a,b) in enumerate(labels))+'</div><button type="button" class="sequence-play" data-play-label="'+('播放流程' if zh else 'Play sequence')+'" data-pause-label="'+('暫停' if zh else 'Pause')+'">'+('播放流程' if zh else 'Play sequence')+'</button></section><script src="'+rel(path,'guide-media.js')+'" defer></script>'

def chapter_path(lang,key):return f'manuals/{lang}/{key}.html'
def write(path,text):
 p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text+'\n')
def heading(title,description,eyebrow='S012Cam'):
 return f'<div class="page-head"><p class="eyebrow">{eyebrow}</p><h1>{html.escape(title)}</h1><p class="lead">{html.escape(description)}</p></div>'
def side(path,lang,key):
 other='zh' if lang=='en' else 'en';group='';body=f'<aside class="manual-nav" aria-label="'+('手冊目錄' if lang=='zh' else 'Manual contents')+'"><h2><a href="'+rel(path,local(lang,'manual'))+'">'+TITLES[lang]['manual']+'</a></h2>'
 for k,t,g in CHAPTERS:
  if group!=g:body+='<h3>'+GROUPS[lang][g]+'</h3>';group=g
  body+='<a href="'+rel(path,chapter_path(lang,k))+'"'+(' aria-current="page"' if key==k else '')+'>'+t[lang]+'</a>'
 return body+'</aside>'
def mobile_contents(path,lang):
 label='章節目錄' if lang=='zh' else 'Chapter contents'
 items=''.join('<a href="'+rel(path,chapter_path(lang,k))+'">'+t[lang]+'</a>' for k,t,g in CHAPTERS)
 return '<details class="manual-mobile-index"><summary>'+label+'</summary><nav aria-label="'+label+'"><a href="'+rel(path,local(lang,'manual'))+'">'+('手冊首頁' if lang=='zh' else 'Manual home')+'</a>'+items+'</nav></details>'

def md_html(text,path):
 out=[];listkind=None
 def close_list():
  nonlocal listkind
  if listkind:out.append('</'+listkind+'>');listkind=None
 for kind,data in blocks(text):
  if kind=='body' and (data.startswith('- ') or re.match(r'^\d+\. ',data)):
   k='ul' if data.startswith('- ') else 'ol'
   if listkind!=k:close_list();out.append('<'+k+'>');listkind=k
   data=re.sub(r'^(?:- |\d+\. )','',data);out.append('<li>'+inline(data)+'</li>');continue
  close_list()
  if kind in ('title','h2','h3'):
   tag={'title':'h1','h2':'h2','h3':'h3'}[kind];out.append(f'<{tag}>{inline(data)}</{tag}>')
  elif kind=='image':
   alt,name=data;src=asset(path,Path(name).name);w,h=PILImage.open(ROOT/'assets'/Path(name).name).size;out.append(f'<figure><a href="{src}"><img src="{src}" alt="{html.escape(alt,quote=True)}" width="{w}" height="{h}" loading="lazy"></a></figure>')
  elif kind=='caption':
   if out and out[-1].endswith('</figure>'):
    number=re.match(r'(?:Fig\.|Figure) (\d+)',data)
    figure=out[-1]
    if number:figure=figure.replace('<figure>',f'<figure id="manual-fig-{number[1]}">',1)
    out[-1]=figure[:-9]+'<figcaption>'+inline(data)+'</figcaption></figure>'
   else:out.append('<p class="caption">'+inline(data)+'</p>')
  elif kind=='table':
   out.append('<div class="table-wrap"><table><thead><tr>'+''.join('<th scope="col">'+inline(c)+'</th>' for c in data[0])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+inline(c)+'</td>' for c in row)+'</tr>' for row in data[1:])+'</tbody></table></div>')
  else:out.append('<p'+(' class="caption"' if kind=='caption' else ' class="note"' if data.startswith(('If the phone does not sense movement','如果手機沒有感應到動作')) else '')+'>'+inline(data)+'</p>')
 close_list();return '\n'.join(out)
def parts(text):
 sections={int(m.group(1)):m.group(0) for m in re.finditer(r'^## (\d+)\..*?(?=^## |\Z)',text,re.M|re.S)}
 sub={}
 for m in re.finditer(r'^### (.*?)\n(.*?)(?=^### |^## |\Z)',sections[8],re.M|re.S):sub[m.group(1)]=m.group(2).strip()
 return sections,sub

def chapter_sources(text,lang):
 sec,sub=parts(text)
 keys={'en':{'handheld':'Case 1. Hold the iPhone and use the Polarizer Rotator','fixed':'Case 2. Use a tripod or secure the iPhone','gyro':'Gyro mode: one shutter press','checks':'Checks and retakes','timer':'Timer mode','alignment':'Align and calculate','hand-polarizer':'Without a Rotator: use a hand-held polarizer'},'zh':{'handheld':'情形一：手持 iPhone，使用 Polarizer Rotator','fixed':'情形二：使用腳架或固定 iPhone','gyro':'Gyro 模式：只按一次快門','checks':'檢查與重拍','timer':'Timer 模式','alignment':'對齊與計算','hand-polarizer':'沒有 Rotator：手持偏振片並手動轉動'}}[lang]
 get=lambda k:sub[keys[k]]
 result={'start':sec[1]+'\n'+sec[2]+'\n'+sec[8].split('###',1)[0], 'assembly':'\n'.join(sec[n] for n in range(3,7)), 'camera':sec[7], 'results':sec[9], 'files':sec[10]+'\n'+sec[11], 'troubleshooting':sec[12]}
 for key in ['handheld','fixed','gyro','timer','alignment','hand-polarizer']:result[key]=get(key)
 result['gyro']+='\n\n### '+keys['checks']+'\n\n'+get('checks')
 return result

def manual_hub(lang,path):
 zh=lang=='zh';a=lambda key:rel(path,chapter_path(lang,key))
 body=heading(TITLES[lang]['manual'],DESCS[lang]['manual'],'S012Cam 2.0')
 body+='<figure class="manual-cover"><a href="'+a('camera')+'"><img src="'+asset(path,'s012cam-camera-numbered.png')+'" alt="'+('實際相機畫面與十二個控制位置' if zh else 'Actual camera screen with twelve numbered controls')+'"></a><figcaption>'+('從實際畫面認識按鈕，再跟著組裝圖與動畫開始量測。' if zh else 'Learn the controls on the actual screen, then follow the assembly illustrations and animation.')+'</figcaption></figure>'
 body+='<div class="manual-jump"><h2>'+('第一次使用？' if zh else 'First measurement?')+'</h2><p>'+('先安裝並檢查偏光片，再選操作方式與拍攝模式。' if zh else 'Fit and check the polarizer, then choose a setup and a capture mode.')+'</p><a class="button" href="'+a('start')+'">'+('從快速開始閱讀' if zh else 'Start with the quick guide')+'</a></div>'
 for title,cards in [(('選擇操作方式' if zh else 'Choose how to support the iPhone'),['handheld','fixed']),(('選擇拍攝模式' if zh else 'Choose a capture mode'),['gyro','timer'])]:
  body+='<section><h2>'+title+'</h2><div class="grid2">'
  notes={'en':{'handheld':'Use both hands and turn the Rotator gently. Alignment is recommended.','fixed':'Use a tripod or a firm support. If nothing moves, calculate without aligning.','gyro':'Turn the dial, then hold still for automatic photos 2–4.','timer':'Turn the dial before the next fixed interval ends. Default: 2 seconds.'},'zh':{'handheld':'雙手握持，輕轉 Rotator。建議對齊後計算。','fixed':'使用腳架或穩固支撐物。手機與場景未移動時，可不對齊直接計算。','gyro':'轉動轉盤後持穩，自動拍攝第 2 至第 4 張。','timer':'固定間隔結束前轉好角度；預設間隔為 2 秒。'}}
  for key in cards:
   label=next(t[lang] for k,t,g in CHAPTERS if k==key)
   body+='<div class="card"><h3>'+label+'</h3><p>'+notes[lang][key]+'</p><a class="more" href="'+a(key)+'">'+('閱讀操作說明' if zh else 'Read the instructions')+'</a></div>'
  body+='</div></section>'
 body+='<section><h2>'+('所有章節' if zh else 'All chapters')+'</h2><ul class="manual-list">'+''.join('<li><a href="'+a(k)+'">'+t[lang]+'</a></li>' for k,t,g in CHAPTERS)+'</ul></section>'
 body+='<div class="download-box"><h2>'+('PDF 與完整網頁版' if zh else 'PDF and full web edition')+'</h2><p>'+('PDF 與網頁章節使用相同的手冊內容。' if zh else 'The PDF and chapter pages use the same manual content.')+'</p><div class="actions"><a class="button" href="'+asset(path,'s012cam-user-manual-zh.pdf')+'" download>繁體中文 PDF</a><a class="button secondary" href="'+asset(path,'s012cam-user-manual-en.pdf')+'" download>English PDF</a></div><p><a href="'+rel(path,f'manuals/S012Cam-user-manual-{lang}.html')+'">'+('閱讀完整網頁版手冊' if zh else 'Read the complete web manual')+'</a></p></div>'
 return body

for lang in ('en','zh'):
 other='zh' if lang=='en' else 'en';text=(ROOT/'manuals'/f'S012Cam-user-manual-{lang}.md').read_text();sources=chapter_sources(text,lang)
 for key in ['home','polarization','app','rotator','manual','buy','support','privacy']:
  path=local(lang,key);title=TITLES[lang][key];desc=DESCS[lang][key]
  if key=='manual':body=manual_hub(lang,path)
  else:
   content=(ROOT/'content'/lang/(key+'.html')).read_text()
   if key=='home':body=content
   else:body=heading(title,desc)+content
   if key=='rotator':
    body=heading(title,desc)+assembly_video(lang,path)+md_html(sources['assembly'],path)
    body+='<div class="actions"><a class="button" href="'+rel(path,local(lang,'buy'))+'">'+('比較 DIY 與完整版' if lang=='zh' else 'Compare DIY and assembled')+'</a><a class="button secondary" href="'+rel(path,chapter_path(lang,'assembly'))+'">'+('閱讀完整組裝與校正章節' if lang=='zh' else 'Full assembly and calibration guide')+'</a><a class="button secondary" href="'+rel(path,local(lang,'manual'))+'">'+('開始拍攝' if lang=='zh' else 'Start capturing')+'</a></div>'
   if key=='support':
    tip=('若 Gyro 停在「Turn to XX」，尚未進入「Hold still」，先轉到提示角度，稍微輕觸或輕敲手機一下，再持穩等待，保持構圖不變。' if lang=='zh' else 'If Gyro stays at “Turn to XX” instead of “Hold still”, turn to the requested angle, lightly touch or gently tap the phone once, then hold still without changing the framing.')
    body=heading(title,desc)+'<section><h2>'+('Gyro 拍攝提示' if lang=='zh' else 'Gyro capture tip')+'</h2><div class="note">'+tip+'</div><a href="'+rel(path,chapter_path(lang,'gyro'))+'">'+('閱讀 Gyro 完整說明' if lang=='zh' else 'Full Gyro instructions')+'</a></section>'+content
  write(path,render(path,lang,title,desc,body,active='' if key in ['home','privacy'] else key,alternate=local(other,key),home=key=='home'))
 for index,(key,titles,group) in enumerate(CHAPTERS):
  path=chapter_path(lang,key);title=titles[lang]
  body=mobile_contents(path,lang)+heading(title,GROUPS[lang][group],TITLES[lang]['manual'])
  source=sources[key]
  # The section label is semantic and stable across both languages.
  if key=='gyro':source=source.replace('### '+('檢查與重拍' if lang=='zh' else 'Checks and retakes'),'### '+('檢查與重拍' if lang=='zh' else 'Checks and retakes'))
  body+=(assembly_video(lang,path) if key=='assembly' else capture_visual(lang,path,key) if key in ('gyro','timer') else '')+md_html(source,path)
  if key in ('handheld','fixed'):body+='<figure><img src="'+asset(path,'s012cam-camera-numbered.png')+'" alt="'+('操作前確認相機控制與量測框' if lang=='zh' else 'Check the camera controls and measurement box before capture')+'"><figcaption>'+('固定構圖，將量測主體保持在虛線框內。' if lang=='zh' else 'Keep the framing fixed and the subject inside the dashed box.')+'</figcaption></figure>'
  if key=='gyro':body=body.replace('<h3>'+('檢查與重拍' if lang=='zh' else 'Checks and retakes')+'</h3>','<h3 id="checks">'+('檢查與重拍' if lang=='zh' else 'Checks and retakes')+'</h3>')
  if key in ('handheld','fixed','hand-polarizer'):
   body+='<div class="note"><p>'+('下一步：選擇拍攝模式，再決定計算方式。' if lang=='zh' else 'Next: choose a capture mode, then the calculation method.')+'</p><p><a href="'+rel(path,chapter_path(lang,'gyro'))+'">Gyro</a> · <a href="'+rel(path,chapter_path(lang,'timer'))+'">Timer</a> · <a href="'+rel(path,chapter_path(lang,'alignment'))+'">'+('對齊與計算' if lang=='zh' else 'Align and calculate')+'</a></p></div>'
  body+='<div class="chapter-next">'
  for j,label in [(index-1,'上一章' if lang=='zh' else 'Previous'),(index+1,'下一章' if lang=='zh' else 'Next')]:
   if 0<=j<len(CHAPTERS):k,t,g=CHAPTERS[j];body+='<a href="'+rel(path,chapter_path(lang,k))+'">'+label+': '+t[lang]+'</a>'
  body+='</div>'
  write(path,render(path,lang,title,title+' — S012Cam 2.0',body,active='manual',alternate=chapter_path(other,key),sidebar=side(path,lang,key)))
 full=f'manuals/S012Cam-user-manual-{lang}.html';body=mobile_contents(full,lang)+assembly_video(lang,full)+'<div class="full-manual">'+md_html(text,full)+'</div>'
 write(full,render(full,lang,TITLES[lang]['manual'],DESCS[lang]['manual'],body,active='manual',alternate=f'manuals/S012Cam-user-manual-{other}.html',sidebar=side(full,lang,'')))
print('Built 16 website pages, 24 manual chapter pages and 2 complete web manuals.')
