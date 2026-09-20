# Bot de consulta OSWork

Ejemplo educativo, determinista, sin API de IA. `/status` confirma ejecución; `/relatorio` suma tres ventas ficticias (R$ 100,00). No recibe comandos de shell.

## Requisitos
Python 3.10+ para el ejemplo; cuenta de Telegram y red de salida HTTPS solo para ejecución real. Un único proceso por token. Datos locales sin secretos en vendas.csv.

## Prueba sin cuenta ni red

```bash
cd materiais/bot
python3 bot.py --self-test
```

Esperado: 11 escenarios offline aprobados. Esto no acredita autenticación o funcionamiento real de Telegram.

## Conectar su cuenta

1. En el BotFather oficial de Telegram, use `/newbot` y guarde el token.
2. Dentro de esta carpeta, copie `.env.example` a `.env`. En Linux/macOS, `chmod 600 .env` restringe la lectura.
3. Edite TELEGRAM_BOT_TOKEN solo en el archivo privado. Nunca pegue el valor en mensajes, Git o capturas de pantalla.
4. Ejecute `python3 bot.py --identify`. Envíe `/start` al bot en una conversación privada y vea el ID numérico en la terminal local. Este modo solo identifica, no responde ni ejecuta tareas.
5. Termine con Ctrl+C y complete ALLOWED_USER_IDS con su ID. No confunda su nombre visible con este identificador. Para varios usuarios autorizados, separe los IDs con coma.
6. Ejecute `python3 bot.py`. Envíe `/status` y `/relatorio`. Verifique el total contra vendas.csv.
7. Termine con Ctrl+C. Sin el proceso en ejecución, no habrá respuesta.

El programa carga solo las dos variables conocidas del .env; las variables ya existentes en el entorno tienen precedencia. No imprime token, URL autenticada ni cuerpo de los mensajes.

## Límites del laboratorio
Long polling dispensa un puerto público de entrada. Si hay un webhook antiguo u otro proceso usando getUpdates, la API puede rechazar la ejecución. Consulte [getUpdates](https://core.telegram.org/bots/api#getupdates) y [deleteWebhook](https://core.telegram.org/bots/api#deletewebhook) antes de modificar una integración existente.

El offset se mantiene en memoria. Un mensaje puede reaparecer después de reiniciar; las funciones de consulta no alteran estado externo. El ejemplo no garantiza entrega exactamente una vez. No lo reutilice para cobros, eliminaciones o envío de documentos sin añadir control de idempotencia y revisión.

Fallos de envío pueden perder una respuesta, ya que el ejemplo avanza el offset al recibir. El usuario puede repetir una consulta. Para producción, diseñe una cola, confirmación y monitoreo según la necesidad.

## Ejecutar en la VPS con systemd

1. Lea el plano-vps.md y la clase de VPS. Use un usuario sin privilegios de root para el proceso.
2. Adapte los cuatro campos de ruta/usuario de la unidad oswork-bot.service.
3. Copie la unidad adaptada a `/etc/systemd/system/oswork-bot.service` con permiso administrativo.
4. Ejecute `sudo systemctl daemon-reload` y `sudo systemctl enable --now oswork-bot`.
5. Verifique `systemctl status oswork-bot --no-pager` y `journalctl -u oswork-bot -n 50 --no-pager`.
6. Pruebe `/status`, reinicie de forma controlada y pruebe de nuevo.
7. Para detener: `sudo systemctl stop oswork-bot`. Para impedir inicio automático: `sudo systemctl disable oswork-bot`.

Restart=on-failure tiene límite de intentos. Los errores persistentes requieren diagnóstico. La supervisión no garantiza disponibilidad.

## Dónde entraría la IA
Añada una función restringida de interpretación o resumen, con entrada mínima, timeout y techo de costo, después de verificar la base. No pase texto recibido como comando de shell. No exponga ejecución irrestricta de Codex. La integración con IA no está implementada en este bot.
