# Bot de consulta OSWork

Exemplo educacional, determinístico, sem API de IA. `/status` confirma execução; `/relatorio` soma três vendas fictícias (R$ 100,00). Não recebe comandos de shell.

## Requisitos
Python 3.10+ para o exemplo; conta Telegram e rede de saída HTTPS apenas para execução real. Um único processo por token. Dados locais sem segredos em vendas.csv.

## Teste sem conta nem rede

```bash
cd materiais/bot
python3 bot.py --self-test
```

Esperado: 11 cenários offline aprovados. Isso não comprova autenticação ou funcionamento real do Telegram.

## Conectar sua conta

1. No BotFather oficial do Telegram, use `/newbot` e guarde o token.
2. Dentro desta pasta, copie `.env.example` para `.env`. No Linux/macOS, `chmod 600 .env` restringe a leitura.
3. Edite TELEGRAM_BOT_TOKEN apenas no arquivo privado. Nunca cole o valor em mensagens, Git ou capturas de tela.
4. Execute `python3 bot.py --identify`. Envie `/start` ao bot em uma conversa privada e veja o ID numérico no terminal local. Este modo só identifica, não responde nem executa tarefas.
5. Encerre com Ctrl+C e preencha ALLOWED_USER_IDS com seu ID. Não confunda seu nome visível com esse identificador. Para vários usuários autorizados, separe IDs com vírgula.
6. Execute `python3 bot.py`. Envie `/status` e `/relatorio`. Confira o total contra vendas.csv.
7. Encerre com Ctrl+C. Sem o processo rodando, não haverá resposta.

O programa carrega somente as duas variáveis conhecidas do .env; variáveis já existentes no ambiente têm precedência. Não imprime token, URL autenticada nem corpo das mensagens.

## Limites do laboratório
Long polling dispensa uma porta pública de entrada. Se houver webhook antigo ou outro processo usando getUpdates, a API pode recusar a execução. Confira [getUpdates](https://core.telegram.org/bots/api#getupdates) e [deleteWebhook](https://core.telegram.org/bots/api#deletewebhook) antes de alterar uma integração existente.

O offset fica em memória. Uma mensagem pode reaparecer após reinício; as funções de consulta não alteram estado externo. O exemplo não garante entrega exatamente uma vez. Não o reutilize para cobranças, exclusões ou envio de documentos sem adicionar controle de idempotência e revisão.

Falhas de envio podem perder uma resposta, pois o exemplo avança o offset ao receber. O usuário pode repetir uma consulta. Para produção, projete fila, confirmação e monitoramento conforme a necessidade.

## Executar na VPS com systemd

1. Leia o plano-vps.md e a aula de VPS. Use usuário sem privilégios de root para o processo.
2. Adapte os quatro campos de caminho/usuário da unidade oswork-bot.service.
3. Copie a unidade adaptada para `/etc/systemd/system/oswork-bot.service` com permissão administrativa.
4. Execute `sudo systemctl daemon-reload` e `sudo systemctl enable --now oswork-bot`.
5. Confira `systemctl status oswork-bot --no-pager` e `journalctl -u oswork-bot -n 50 --no-pager`.
6. Teste `/status`, reinicie de forma controlada e teste de novo.
7. Para parar: `sudo systemctl stop oswork-bot`. Para impedir início automático: `sudo systemctl disable oswork-bot`.

Restart=on-failure tem limite de tentativas. Erros persistentes precisam de diagnóstico. Supervisão não é garantia de disponibilidade.

## Onde a IA entraria
Adicione uma função restrita de interpretação ou resumo, com entrada mínima, timeout e teto de custo, depois de verificar a base. Não passe texto recebido como comando de shell. Não exponha execução irrestrita de Codex. A integração com IA não está implementada neste bot.
