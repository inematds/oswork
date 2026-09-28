#!/usr/bin/env python3
"""Generate cached translations; never used at course runtime.
Motor principal: Codex pela assinatura (codex exec -m gpt-6-luna). Reserva: Groq, só quando o Codex falha."""
import json,os,re,time,urllib.request,urllib.error,sys,subprocess,tempfile
CODEX_MODEL=os.environ.get("CODEX_MODEL","gpt-6-luna")
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def codex_json(system,user):
 with tempfile.TemporaryDirectory() as d:
  out=Path(d)/'out.txt'
  codex=os.environ.get('CODEX_BIN') or next((c for c in [os.path.expanduser('~/.npm-global/bin/codex')] if os.path.exists(c)),'codex')
  env={**os.environ,'PATH':os.path.dirname(codex)+':'+os.environ.get('PATH','')}
  r=subprocess.run([codex,'exec','-m',CODEX_MODEL,'--skip-git-repo-check','--ephemeral','--sandbox','read-only','-C',d,'-o',str(out),'-'],
   input=system+'\n\nReturn ONLY the JSON object (no code fences).\nINPUT JSON:\n'+user,text=True,capture_output=True,timeout=900,env=env)
  if r.returncode or not out.exists():raise RuntimeError(f'codex exec rc={r.returncode}: {r.stderr[-200:]}')
  t=re.sub(r'^```(?:json)?\s*|\s*```$','',out.read_text().strip())
 return json.loads(t[t.index('{'):t.rindex('}')+1])

def key():
 for p in [Path.home()/'projetos/openpcbotv2/.env',Path.home()/'projetos/wifi/.env']:
  if p.exists():
   m=re.search(r'^GROQ_API_KEY=[\"\']?([^\"\'\n]+)',p.read_text(),re.M)
   if m:return m[1].strip()
 return None   # sem chave: sem reserva Groq, só o Codex

def limit(detail):
 p=Path.home()/'projetos/wifi/LIMITES.md';s=p.read_text();line=f'| 2026-09-20 | Traduzir OSWork via Groq | {detail} | Retentativa com espera e cache | Respeitar limites da conta | aceito |\n'
 if line not in s:p.write_text(s.split('\n',1)[0]+'\n\n'+line+s.split('\n',1)[1])

def translate(lang):
 source=json.loads((ROOT/'i18n/source.json').read_text());path=ROOT/f'i18n/{lang}.json';cache=json.loads(path.read_text()) if path.exists() else {}
 missing=[(k,v) for k,v in source.items() if k not in cache];batches=[];batch={};size=0
 for k,v in missing:
  if size+len(v['source'])>3000 and batch:batches.append(batch);batch={};size=0
  batch[k]=v;size+=len(v['source'])
 if batch:batches.append(batch)
 secret=key();name={'en':'clear natural English','es':'neutral international Spanish'}[lang]
 for idx,batch in enumerate(batches,1):
  ids={str(i):k for i,k in enumerate(batch)}
  payload={i:batch[k] for i,k in ids.items()}
  body={'model':'openai/gpt-oss-120b','temperature':0.15,'reasoning_effort':'low','max_completion_tokens':4000,'response_format':{'type':'json_object'},'messages':[{'role':'system','content':f'You are a careful professional educational translator. Translate ALL provided Portuguese content into {name}. Do not summarize, omit, add content or change technical facts. Return a JSON object mapping each exact input ID to its translated string, no other keys. The input values include kind and source; output values must be strings only. Preserve Markdown formatting, code fences, indentation/newlines in pre/markdown. Preserve EVERY file name, folder name, path, URL, identifier, environment variable, product/model name, command syntax and command arguments exactly (including Portuguese paths such as projetos, entradas, saidas, memoria.md, relatorio-semanal, vendas.csv, ALLOWED_USER_IDS, .env.example). Do NOT translate names inside paths. Translate explanatory prose and comments. Translate UI labels naturally. OSWork is the product name, never translate it. The dates and numbers must stay unchanged. Keep all sentences and examples. For shell blocks, keep commands exact; translate comments only. The course is an educational sandbox; do not embellish claims.'},{'role':'user','content':json.dumps(payload,ensure_ascii=False)}]}
  def check(raw):
   if set(raw)!=set(ids):raise ValueError('Translation IDs mismatch')
   out={ids[k]:v for k,v in raw.items()}
   if set(out)!=set(batch) or any(not isinstance(v,str) or not v.strip() for v in out.values()):raise ValueError('Translation schema mismatch')
   for k,v in out.items():
    if len(batch[k]['source'])>200 and len(v)<len(batch[k]['source'])*.48:raise ValueError('Translation unexpectedly shortened')
   return out
  codex_ok=False
  for tent in range(2):
   try:
    out=check(codex_json(body['messages'][0]['content'],body['messages'][1]['content']))
    cache.update(out);path.write_text(json.dumps(cache,ensure_ascii=False,indent=2)+'\n');print(lang,idx,'/',len(batches),'cached',len(cache),'codex',CODEX_MODEL,flush=True)
    codex_ok=True;break
   except (RuntimeError,ValueError,subprocess.TimeoutExpired) as e:print(lang,'codex falhou',tent+1,str(e)[:120],flush=True)
  if not codex_ok and not secret:raise SystemExit('Codex falhou e não há GROQ_API_KEY de reserva; cache preservado.')
  for attempt in range(6):
   if codex_ok:break
   req=urllib.request.Request('https://api.groq.com/openai/v1/chat/completions',data=json.dumps(body).encode(),headers={'Authorization':'Bearer '+secret,'Content-Type':'application/json','User-Agent':'OSWork-localizer/1.0'})
   try:
    with urllib.request.urlopen(req,timeout=60) as response:result=json.load(response)
    content=result['choices'][0]['message']['content'];raw=json.loads(content)
    if set(raw)!=set(ids):raise ValueError('Translation IDs mismatch')
    out={ids[k]:v for k,v in raw.items()}
    if set(out)!=set(batch) or any(not isinstance(v,str) or not v.strip() for v in out.values()):raise ValueError('Translation schema mismatch')
    # Code and URL preservation checked during review; count/length protects omissions.
    for k,v in out.items():
     if len(batch[k]['source'])>200 and len(v)<len(batch[k]['source'])*.48:raise ValueError('Translation unexpectedly shortened')
    cache.update(out);path.write_text(json.dumps(cache,ensure_ascii=False,indent=2)+'\n');print(lang,idx,'/',len(batches),'cached',len(cache),'usage',result.get('usage',{}).get('total_tokens'),flush=True);break
   except urllib.error.HTTPError as e:
    if e.code==429:
     limit('HTTP 429: limite de consumo');wait=min(60,20*(attempt+1));print(lang,'rate limit; retry in',wait,flush=True);time.sleep(wait)
    else:limit(f'HTTP {e.code}');raise SystemExit(f'Groq HTTP {e.code}; no credentials printed') from None
   except (ValueError,TimeoutError,urllib.error.URLError) as e:
    print(lang,'retry',attempt+1,type(e).__name__,str(e)[:120],flush=True); (ROOT/'.verificacao/translation-last.json').write_text(json.dumps(result,ensure_ascii=False,indent=2) if 'result' in locals() else '{}');time.sleep(3)
  else:raise SystemExit('Translation did not succeed after six attempts; cache preserved.')
  # Small paced batches; process runs separately so the main turn stays responsive.
  if idx<len(batches) and not codex_ok:time.sleep(25)   # pausa só para a cota da Groq
if __name__=='__main__':
 for lang in sys.argv[1:] or ['es','en']:translate(lang)
