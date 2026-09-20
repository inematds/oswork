# OSWork query bot

Educational example, deterministic, without AI API. `/status` confirms execution; `/relatorio` sums three fictional sales (R$ 100,00). Does not accept shell commands.

## Requirements
Python 3.10+ for the example; Telegram account and HTTPS outbound network only for real execution. A single process per token. Local data without secrets in vendas.csv.

## Test without account or network

```bash
cd materiais/bot
python3 bot.py --self-test
```

Expected: 11 offline scenarios approved. This does not prove authentication or real Telegram operation.

## Connect your account

1. In the official Telegram BotFather, use `/newbot` and keep the token.
2. Inside this folder, copy `.env.example` to `.env`. On Linux/macOS, `chmod 600 .env` restricts reading.
3. Edit TELEGRAM_BOT_TOKEN only in the private file. Never paste the value in messages, Git, or screenshots.
4. Run `python3 bot.py --identify`. Send `/start` to the bot in a private chat and see the numeric ID in the local terminal. This mode only identifies, does not respond or execute tasks.
5. Exit with Ctrl+C and fill ALLOWED_USER_IDS with your ID. Do not confuse your visible name with this identifier. For multiple authorized users, separate IDs with commas.
6. Run `python3 bot.py`. Send `/status` and `/relatorio`. Check the total against vendas.csv.
7. Exit with Ctrl+C. Without the process running, there will be no response.

The program loads only the two known variables from .env; existing environment variables take precedence. It does not print the token, authenticated URL, or message bodies.

## Laboratory limits
Long polling does not require a public inbound port. If there is an old webhook or another process using getUpdates, the API may reject execution. Check [getUpdates](https://core.telegram.org/bots/api#getupdates) and [deleteWebhook](https://core.telegram.org/bots/api#deletewebhook) before altering an existing integration.

The offset stays in memory. A message may reappear after a restart; the query functions do not change external state. The example does not guarantee exactly‑once delivery. Do not reuse it for charges, deletions, or document sending without adding idempotency control and review.

Send failures may lose a response, as the example advances the offset upon receipt. The user may repeat a query. For production, design a queue, acknowledgment, and monitoring as needed.

## Run on VPS with systemd

1. Read plano-vps.md and the VPS lesson. Use a non‑root user for the process.
2. Adapt the four path/user fields of the oswork-bot.service unit.
3. Copy the adapted unit to `/etc/systemd/system/oswork-bot.service` with administrative permission.
4. Run `sudo systemctl daemon-reload` and `sudo systemctl enable --now oswork-bot`.
5. Check `systemctl status oswork-bot --no-pager` and `journalctl -u oswork-bot -n 50 --no-pager`.
6. Test `/status`, restart in a controlled way and test again.
7. To stop: `sudo systemctl stop oswork-bot`. To prevent automatic start: `sudo systemctl disable oswork-bot`.

Restart=on-failure has a retry limit. Persistent errors need diagnosis. Supervision is not a guarantee of availability.

## Where AI would fit
Add a restricted interpretation or summarization function, with minimal input, timeout, and cost ceiling, after verifying the base. Do not pass received text as a shell command. Do not expose unrestricted Codex execution. AI integration is not implemented in this bot.