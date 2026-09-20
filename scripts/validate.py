#!/usr/bin/env python3
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,zipfile
ROOT=Path(__file__).resolve().parents[1]
class Parse(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.links=[];self.topics=[];self.scripts=[];self.cur=None;self.svg=0;self.meta={}
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag in ('a','link','script','iframe'):
   v=a.get('href',a.get('src'))
   if v:self.links.append(v)
  if 'data-inema-topic' in a:self.topics.append(a['data-inema-topic'])
  if tag=='svg':self.svg+=1
  if tag=='meta':self.meta[a.get('name')]=a.get('content')
  if tag=='script' and 'data-inema-manifest' in a:self.cur=''
 def handle_data(self,s):
  if self.cur is not None:self.cur+=s
 def handle_endtag(self,tag):
  if tag=='script' and self.cur is not None:self.scripts.append(json.loads(self.cur));self.cur=None
pages={}
for path in ROOT.rglob('*.html'):
 if '.verificacao' in path.parts or 'capa' in path.parts:continue
 p=Parse();p.feed(path.read_text());pages[path]=p
errors=[]
for path,p in pages.items():
 if len(p.ids)!=len(set(p.ids)):errors.append(f'IDs duplicados: {path}')
 locale=path.relative_to(ROOT).parts[0]
 if p.meta.get('inema-course')!=('oswork-v2-'+locale if locale in ('en','es') else 'oswork-v2'):errors.append(f'Meta ausente: {path}')
 if len(p.scripts)!=1:errors.append(f'Manifesto ausente: {path}')
 for link in p.links:
  u=urlsplit(link)
  if u.scheme or u.netloc:continue
  target=(path.parent/unquote(u.path)).resolve() if u.path else path
  if not target.exists():errors.append(f'Link ausente: {path.name}: {link}')
  if u.fragment and target in pages and u.fragment not in pages[target].ids:errors.append(f'Âncora ausente: {path.name}: {link}')
 if path.name.startswith('modulo-'):
  if len(p.topics)!=6:errors.append(f'Tópicos inválidos: {path}')
  if not p.svg:errors.append(f'Diagrama ausente: {path}')
 for manifest in p.scripts:
  for track in manifest['tracks']:
   for module in track['modules']:
    target=(path.parent/module['href']).resolve()
    if target not in pages or len(pages[target].topics)!=module['topics']:errors.append(f'Manifesto divergente: {path}')
assert not errors,'\n'.join(errors)
for prefix in ('','es','en'):
 with zipfile.ZipFile(ROOT/prefix/'materiais/oswork-kit.zip') as z:
  assert not any(Path(n).name=='.env' for n in z.namelist())
  assert 'bot/bot.py' in z.namelist()
  assert 'bot/.env.example' in z.namelist()
assert len(pages)==42, f'Expected 42 pages, got {len(pages)}'
count=sum(len(p.topics) for p in pages.values());assert count==144
print(f'OK: {len(pages)} páginas, {count} tópicos em três idiomas, IDs, links locais, âncoras, manifestos e kits sem .env privado.')
