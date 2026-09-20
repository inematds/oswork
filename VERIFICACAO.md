# Verificação — 20/09/2026

- `python3 scripts/validate.py`: 14 páginas e 48 tópicos; links locais, âncoras, IDs, manifesto e kit aprovados.
- `python3 materiais/bot/bot.py --self-test`: 11 cenários offline aprovados.
- `node --check assets/learn.js` e `node --check assets/site.js`: sintaxe válida.
- `node scripts/browser-test.cjs`: 13 grupos aprovados em Chromium; sem erros de JavaScript.
- Navegador: progresso entre páginas, persistência após recarga, dúvida, grifo, campos adicionais de importação, rejeição de importação inválida, retomada, acordeão, modal, tema claro, celular sem transbordamento horizontal, armazenamento bloqueado e conteúdo legível sem JavaScript.
- Revisão visual: página inicial em desktop e celular, tema claro e capa 1280×720.
- Módulos com seis tópicos, três seções conceituais por tópico, diagramas SVG, práticas e gabaritos; HTML legível com mais de 500 linhas por módulo.

## Limites observados

Os testes do bot usam dados fictícios e não fazem chamadas reais ao Telegram. Não foi contratada nem alterada uma VPS. A instalação do Codex, autenticação e integração real pertencem às práticas do aluno. Progresso entre arquivos abertos diretamente por file:// depende do navegador; prefira servidor HTTP local.

## Capa

Skill capa-inema, engine local inemaimg, modelo flux2-klein. Cena: uma mesa profissional organizada com notebook, pastas, caderno, calendário e pequeno servidor. Saída: capa/capa.png; base: capa/base.png. Nenhuma geração de imagem acontece no navegador do aluno.

## Publicação

Push origin/main confirmado. GitHub Pages configurado em main /, build built sem erro e página inicial HTTP 200 em 20/09/2026.
