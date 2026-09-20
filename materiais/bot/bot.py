#!/usr/bin/env python3
"""Bot didático restrito. Biblioteca padrão; nenhum shell ou modelo de IA."""
import argparse,csv,json,os,time,logging,urllib.request,urllib.error
from decimal import Decimal,InvalidOperation
from pathlib import Path
BASE=Path(__file__).resolve().parent
LOG=logging.getLogger('oswork')

def load_env(path):
    if not path.exists():return
    for line in path.read_text().splitlines():
        line=line.strip()
        if not line or line.startswith('#'):continue
        key,sep,value=line.partition('=')
        if sep and key in ('TELEGRAM_BOT_TOKEN','ALLOWED_USER_IDS'):
            os.environ.setdefault(key,value.strip().strip('"').strip("'"))

def report(path):
    total=Decimal('0');count=0
    with path.open(newline='',encoding='utf-8') as stream:
        reader=csv.DictReader(stream)
        if reader.fieldnames!=['produto','valor']:raise ValueError('Cabeçalho inválido')
        for row in reader:
            if not row.get('produto') or None in row:raise ValueError('Linha inválida')
            try:value=Decimal(row['valor'])
            except (InvalidOperation,TypeError):raise ValueError('Valor inválido') from None
            if not value.is_finite() or value<0 or value!=value.quantize(Decimal('.01')):
                raise ValueError('Valor monetário inválido')
            total+=value;count+=1
    if not count:raise ValueError('Sem registros')
    return f'Dados fictícios de treino: {count} vendas; total R$ {total:.2f}. Sem chamada de IA.'

def handle_message(message,allowed,data_path=BASE/'vendas.csv'):
    if message.get('chat',{}).get('type')!='private':return None
    if message.get('from',{}).get('id') not in allowed:return None
    command=message.get('text','').strip()
    if command in ('/start','/help'):return 'OSWork: comandos permitidos /status e /relatorio. Dados fictícios; não executa mensagens como comandos.'
    if command=='/status':return 'OSWork ativo. Acesso restrito. Bot determinístico de treino.'
    if command=='/relatorio':
        try:return report(data_path)
        except (OSError,ValueError,InvalidOperation):return 'Não foi possível validar vendas.csv. Confira o arquivo local; nenhum total foi inventado.'
    return 'Comando desconhecido. Use /status ou /relatorio.'

def api(token,method,data):
    req=urllib.request.Request(f'https://api.telegram.org/bot{token}/{method}',data=json.dumps(data).encode(),headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(req,timeout=35) as response:result=json.load(response)
    if not result.get('ok'):raise RuntimeError('Telegram recusou operação')
    return result['result']

def self_test():
    import tempfile
    def msg(text,uid=42,kind='private'):return {'from':{'id':uid},'chat':{'id':uid,'type':kind},'text':text}
    assert 'ativo' in handle_message(msg('/status'),{42})
    assert handle_message(msg('/status',99),{42}) is None
    assert handle_message(msg('/status',kind='group'),{42}) is None
    assert 'desconhecido' in handle_message(msg('cat /etc/passwd'),{42})
    assert '100.00' in handle_message(msg('/relatorio'),{42})
    with tempfile.TemporaryDirectory() as d:
        p=Path(d)/'vendas.csv'
        assert 'Não foi possível' in handle_message(msg('/relatorio'),{42},p)
        for value in ('produto,valor\n','produto,valor\nA,NaN\n','produto,valor\nA,-1\n','produto,valor\nA,texto\n','produto,valor\nA,1.001\n'):
            p.write_text(value)
            assert 'Não foi possível' in handle_message(msg('/relatorio'),{42},p)
    print('OK: 11 cenários offline — acesso, grupo, comando, soma e arquivos inválidos.')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test',action='store_true');parser.add_argument('--identify',action='store_true')
    args=parser.parse_args()
    if args.self_test:self_test();return
    load_env(BASE/'.env')
    token=os.environ.get('TELEGRAM_BOT_TOKEN','')
    if not token or token=='preencha_localmente':parser.error('Configure TELEGRAM_BOT_TOKEN no .env privado.')
    try:allowed={int(x.strip()) for x in os.environ.get('ALLOWED_USER_IDS','').split(',') if x.strip()}
    except ValueError:parser.error('ALLOWED_USER_IDS deve conter IDs numéricos separados por vírgula.')
    if not allowed and not args.identify:parser.error('Configure pelo menos um ID permitido.')
    logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s')
    offset=0;delay=2
    if args.identify:print('Identificação apenas: envie /start em privado; confira seu ID abaixo e encerre com Ctrl+C. Nenhuma função operacional ativa.',flush=True)
    while True:
        try:
            updates=api(token,'getUpdates',{'offset':offset,'timeout':25,'allowed_updates':['message']})
            for update in updates:
                offset=max(offset,update['update_id']+1)
                m=update.get('message',{})
                if args.identify:
                    if m.get('text')=='/start' and m.get('chat',{}).get('type')=='private':
                        print('ID recebido na identificação:',m.get('from',{}).get('id'),flush=True)
                    continue
                reply=handle_message(m,allowed)
                if reply:api(token,'sendMessage',{'chat_id':m['chat']['id'],'text':reply})
            delay=2
        except urllib.error.HTTPError as e:
            LOG.warning('Falha HTTP %s no Telegram; sem detalhes que exponham token.',e.code)
            if e.code in (401,404,409):
                LOG.error('Confira token, instância duplicada ou webhook; processo encerrado para diagnóstico.');raise SystemExit(1)
            time.sleep(delay);delay=min(delay*2,60)
        except (urllib.error.URLError,TimeoutError,OSError,ValueError,RuntimeError):
            LOG.warning('Falha de rede ou resposta; nova tentativa em %s segundos.',delay)
            time.sleep(delay);delay=min(delay*2,60)
        except KeyboardInterrupt:print('Bot encerrado.');return
if __name__=='__main__':main()
