#!/usr/bin/env python3
"""Render cached English/Spanish editions offline. Run build.py first."""
from localization import *
import shutil,os,zipfile,textwrap
BASE='https://inematds.github.io/oswork/'
LANGS={'pt':('pt-BR','Português'),'es':('es','Español'),'en':('en','English')}

def language_links(soup,rel,lang):
 for old in soup.select('[data-os-languages],link[rel="canonical"],link[rel="alternate"][hreflang]'):old.decompose()
 folder='' if lang=='pt' else lang+'/'
 for code,(locale,label) in LANGS.items():
  prefix='' if code=='pt' else code+'/'
  soup.head.append(soup.new_tag('link',rel='alternate',hreflang=locale,href=BASE+prefix+rel.as_posix()))
 soup.head.append(soup.new_tag('link',rel='alternate',hreflang='x-default',href=BASE+rel.as_posix()))
 soup.head.append(soup.new_tag('link',rel='canonical',href=BASE+folder+rel.as_posix()))
 nav=soup.new_tag('div',attrs={'class':'language-nav','data-os-languages':'','aria-label':{'pt':'Idioma do curso','es':'Idioma del curso','en':'Course language'}[lang]})
 for code,(locale,label) in LANGS.items():
  target=ROOT/('' if code=='pt' else code)/rel
  href=os.path.relpath(target,(ROOT/folder/rel).parent).replace(os.sep,'/')
  a=soup.new_tag('a',href=href,hreflang=locale,lang=locale);a.string=label
  if code==lang:a['aria-current']='page'
  nav.append(a)
 soup.select_one('.nav-tracks').insert_after(nav)

def wrap_diagrams(soup):
 for text in soup.select('svg text[font-size="14"]'):
  label=text.get_text()
  if len(label)<=27:continue
  lines=textwrap.wrap(label,31,break_long_words=False,break_on_hyphens=False)
  text.clear();text['font-size']='11';y=float(text['y'])-10
  for i,line in enumerate(lines):
   span=soup.new_tag('tspan',x=text['x'],y=str(y+i*11));span.string=line;text.append(span)

def render(lang):
 cache=json.loads((ROOT/f'i18n/{lang}.json').read_text())
 cache.update(json.loads((ROOT/f'i18n/review-{lang}.json').read_text()))
 ui_static=json.loads((ROOT/f'i18n/ui-{lang}.json').read_text())
 comments=json.loads((ROOT/f'i18n/comments-{lang}.json').read_text())
 def tr(s,kind='text'):
  value=norm(s) if kind=='text' else s
  if not eligible(value):return s
  key=ident(value)
  if value in ui_static:return ui_static[value]
  if key not in cache and ' → ' in value:return ' → '.join(tr(part) for part in value.split(' → '))
  if key not in cache:raise ValueError(f'Missing {lang} translation: {value[:90]}')
  return cache[key]
 for path in pages():
  rel=path.relative_to(ROOT);soup=prepare_soup(BeautifulSoup(path.read_text(),'html.parser'))
  # PT language nav is regenerated independently below.
  for old in soup.select('[data-os-languages]'):old.decompose()
  for n in list(text_nodes(soup)):
   original=str(n);value=tr(original,'pre' if n.find_parent('pre') else 'text')
   if not n.find_parent('pre'):
    value=(' ' if original[:1].isspace() else '')+value+(' ' if original[-1:].isspace() else '')
   n.replace_with(NavigableString(value))
  for tag in soup.find_all(True):
   for a in ATTRS:
    if tag.get(a):tag[a]=tr(tag[a])
   if tag.name=='meta' and (tag.get('name')=='description' or tag.get('property')=='og:title'):tag['content']=tr(tag['content'])
  for pre in soup.find_all('pre'):
   content=pre.get_text()
   for a,b in comments.items():content=content.replace(a,b)
   pre.clear();pre.string=content
  soup.html['lang']=lang;soup.select_one('meta[name="inema-course"]')['content']='oswork-v2-'+lang
  soup.select_one('meta[property="og:image"]')['content']=BASE+lang+'/capa/capa.png'
  manifest_tag=soup.select_one('[data-inema-manifest]');manifest=json.loads(manifest_tag.string);manifest['course']='oswork-v2-'+lang
  for track in manifest['tracks']:
   track['title']=tr(track['title'])
   for mod in track['modules']:mod['title']=tr(mod['title'])
  manifest_tag.string=json.dumps(manifest,ensure_ascii=False)
  wrap_diagrams(soup)
  language_links(soup,rel,lang)
  target=ROOT/lang/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(str(soup))
 dest=ROOT/lang
 shutil.copytree(ROOT/'assets',dest/'assets',dirs_exist_ok=True)
 ui=json.loads((ROOT/f'i18n/ui-{lang}.json').read_text());tokens=json.loads((ROOT/'i18n/js-strings.json').read_text())
 for file,items in tokens.items():
  src=(ROOT/file).read_text()
  for token in items:
   literal=src[token['start']:token['end']]
   if len(literal)<2 or literal[0] not in ('\"',"'",'`') or literal[-1]!=literal[0]:raise ValueError('JS token cache is stale; run node scripts/extract-js-strings.cjs')
  for token in sorted(items,key=lambda t:t['start'],reverse=True):
   if token['value'] in ui:src=src[:token['start']]+json.dumps(ui[token['value']],ensure_ascii=False)+src[token['end']:]
  src=src.replace('inema.oswork-v2.meta','inema.oswork-v2-'+lang+'.meta').replace('oswork.task.','oswork.'+lang+'.task.')
  labels={'en':{'todas':'all','yellow':'yellow','green':'green','blue':'blue','pink':'pink','doubt':'question'},'es':{'todas':'todos','yellow':'amarillo','green':'verde','blue':'azul','pink':'rosa','doubt':'duda'}}[lang]
  src=src.replace(json.dumps(ui['Marcar com cor '],ensure_ascii=False)+' + c',json.dumps(ui['Marcar com cor '],ensure_ascii=False)+' + '+json.dumps(labels,ensure_ascii=False)+'[c]')
  src=src.replace('o.textContent = c;', 'o.textContent = '+json.dumps(labels,ensure_ascii=False)+'[c];')
  src=src.replace("'inema-journey__tag', 'duvida'","'inema-journey__tag', "+json.dumps('question' if lang=='en' else 'duda'))
  (dest/file).write_text(src)
 for p in (ROOT/'materiais').rglob('*'):
  if not p.is_file() or p.suffix in ('.html','.zip','.pyc') or '__pycache__' in p.parts:continue
  target=dest/p.relative_to(ROOT);target.parent.mkdir(parents=True,exist_ok=True)
  if p.suffix=='.md':target.write_text(tr(p.read_text(),'markdown'))
  else:shutil.copy2(p,target)
 unit=dest/'materiais/bot/oswork-bot.service';unit_text=unit.read_text()
 for a,b in comments.items():unit_text=unit_text.replace(a,b)
 unit.write_text(unit_text)
 (dest/'FONTES.md').write_text(tr((ROOT/'FONTES.md').read_text(),'markdown'))
 # Keep commands and CSV schema identical; translate user-facing bot responses and checks.
 bot=dest/'materiais/bot/bot.py';src=bot.read_text();mapping=json.loads((ROOT/f'i18n/bot-{lang}.json').read_text())
 for a,b in sorted(mapping.items(),key=lambda kv:len(kv[0]),reverse=True):src=src.replace(a,b)
 bot.write_text(src)
 with zipfile.ZipFile(dest/'materiais/oswork-kit.zip','w',zipfile.ZIP_DEFLATED) as z:
  for p in sorted((dest/'materiais').rglob('*')):
   if p.is_file() and p.suffix not in ('.html','.zip','.pyc') and '__pycache__' not in p.parts:z.write(p,p.relative_to(dest/'materiais'))
 print(lang,': 14 pages + localized UI and kit')
if __name__=='__main__':
 for lang in ('es','en'):render(lang)
 for p in pages():
  soup=BeautifulSoup(p.read_text(),'html.parser');wrap_diagrams(soup);language_links(soup,p.relative_to(ROOT),'pt');p.write_text(str(soup))
