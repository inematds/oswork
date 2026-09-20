#!/usr/bin/env python3
"""Check complete translations, course structure, language links and technical tokens."""
from localization import *
from urllib.parse import urlsplit
from collections import Counter
source=json.loads((ROOT/'i18n/source.json').read_text());errors=[]
for lang in ('en','es'):
 p=ROOT/f'i18n/{lang}.json'
 if not p.exists():errors.append(f'{lang}: missing cache');continue
 cache=json.loads(p.read_text());cache.update(json.loads((ROOT/f'i18n/review-{lang}.json').read_text()))
 for key,item in source.items():
  if key not in cache:errors.append(f'{lang}: missing segment {key}');continue
  # Executable interfaces must survive translation; detect accidental file renames.
  tokens=set(re.findall(r'\b[\w-]+\.(?:md|py|csv|json|txt|toml|zip)\b|\b(?:OPENAI_API_KEY|TELEGRAM_BOT_TOKEN|ALLOWED_USER_IDS|DATABASE_URL)\b|https?://[^\s)<>]+',item['source']))
  for token in tokens:
   if token not in cache[key]:errors.append(f'{lang}: lost technical token {token} in {key}')
 for path in pages():
  rel=path.relative_to(ROOT);target=ROOT/lang/rel
  if not target.exists():errors.append(f'{lang}: missing page {rel}');continue
  original=BeautifulSoup(path.read_text(),'html.parser');soup=BeautifulSoup(target.read_text(),'html.parser')
  assert soup.html['lang']==lang
  assert len(soup.select('[data-inema-topic]'))==len(original.select('[data-inema-topic]'))
  assert len(soup.select('[data-os-languages] a'))==3
  for a in soup.select('[data-os-languages] a'):
   dest=(target.parent/a['href']).resolve();assert dest.exists(),str(dest)
   assert dest.relative_to(ROOT).as_posix().endswith(rel.as_posix())
  assert soup.select_one('link[rel="canonical"]')['href']=='https://inematds.github.io/oswork/'+lang+'/'+rel.as_posix()
  assert len(soup.select('link[rel="alternate"][hreflang]'))==4
  # Pure command lines are deliberately identical across all languages.
  def commands(s):
   return [line for pre in s.find_all('pre') for line in pre.get_text().splitlines() if re.match(r'^(?:git |codex(?: |$)|python3 |sudo |systemctl |journalctl |mkdir |cd |cp |chmod |pwd$)',line)]
  assert commands(soup)==commands(original),(lang,rel,'commands changed')
assert not errors,'\n'.join(errors)
print('OK: complete EN/ES dictionaries; technical filenames; same topics/commands; language routes and canonical links.')
