#!/usr/bin/env python3
"""Offline catalog extraction/rendering. Translation API is opt-in in translate.py."""
from pathlib import Path
from bs4 import BeautifulSoup,Comment,Doctype,NavigableString
import json,re,hashlib
ROOT=Path(__file__).resolve().parents[1]
ATTRS=('aria-label','title','alt')
def norm(s):return re.sub(r'\s+',' ',str(s)).strip()
def ident(s):return hashlib.sha256(s.encode()).hexdigest()[:16]
def pages():return [ROOT/'index.html',*sorted((ROOT/'curso').rglob('*.html')),ROOT/'materiais/index.html']
def eligible(s):return bool(re.search(r'[A-Za-zÀ-ÿ]',s)) and s not in ('OSWork','OSWork_','INEMA.CLUB','OSWORK','PT','EN','ES')
def text_nodes(soup):
 for n in soup.find_all(string=True):
  if isinstance(n,(Comment,Doctype)) or n.parent.name in ('script','style','noscript'):continue
  # Shell commands and file trees retain executable identifiers. Instruction templates translate.
  pre=n.find_parent('pre')
  if pre and re.search(r'^(?:mkdir |git |python3 |sudo |~/projetos/)',str(n)):continue
  if eligible(norm(n)):yield n

def prepare_soup(soup):
 for nav in soup.select('[data-os-languages]'):nav.decompose()
 for text in soup.select('svg text'):
  spans=text.find_all('tspan')
  if spans:
   label=' '.join(span.get_text() for span in spans);text.clear();text.string=label;text['font-size']='14'
 return soup

def catalog():
 out={}
 def add(s,kind='text'):
  s=norm(s) if kind=='text' else s
  if eligible(s):out[ident(s)]={'source':s,'kind':kind}
 for path in pages():
  soup=prepare_soup(BeautifulSoup(path.read_text(),'html.parser'))
  for n in text_nodes(soup):add(str(n),'pre' if n.find_parent('pre') else 'text')
  for tag in soup.find_all(True):
   for a in ATTRS:
    if tag.get(a):add(tag[a])
   if tag.name=='meta' and (tag.get('name')=='description' or tag.get('property')=='og:title'):add(tag['content'])
  manifest=json.loads(soup.select_one('[data-inema-manifest]').string)
  for tr in manifest['tracks']:
   add(tr['title'])
   for m in tr['modules']:add(m['title'])
 for p in (ROOT/'materiais').rglob('*.md'):add(p.read_text(),'markdown')
 add((ROOT/'FONTES.md').read_text(),'markdown')
 return out
if __name__=='__main__':
 out=catalog();(ROOT/'i18n/source.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(len(out),'unique segments;',sum(len(v['source']) for v in out.values()),'characters')
