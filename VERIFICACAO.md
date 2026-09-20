# Verificação — 20/09/2026

- `python3 scripts/validate.py`: 14 páginas e 48 tópicos; links locais, âncoras, IDs, manifesto e kit aprovados.
- `python3 materiais/bot/bot.py --self-test`: 11 cenários offline aprovados.
- `node --check assets/learn.js` e `node --check assets/site.js`: sintaxe válida.
- `node scripts/browser-test.cjs`: 13 grupos aprovados em Chromium; sem erros de JavaScript.
- Navegador: progresso entre páginas, persistência após recarga, dúvida, grifo, campos adicionais de importação, rejeição de importação inválida, retomada, acordeão, modal, tema claro, celular sem transbordamento horizontal, armazenamento bloqueado e conteúdo legível sem JavaScript.
- Revisão visual: página inicial em desktop e celular, tema claro e capa 1280×720.
- Módulos com seis tópicos, três seções conceituais por tópico, diagramas SVG, práticas e gabaritos; HTML legível com mais de 500 linhas por módulo.

## Ampliação multilíngue 1.1.0

- Português: 13 grupos de teste de navegador continuam aprovados após correção de persistência imediata do checkpoint.
- Espanhol: 14 páginas geradas; testes de interface traduzida, armazenamento isolado, rejeição de importação de outro idioma, notas persistentes, checklist, retomada, links de idioma, celular e leitura sem JavaScript aprovados. Bot: 11 cenários offline aprovados.
- Portal: nove testes e build Next.js aprovados; base de conteúdo: 41 testes aprovados. Pushes PT confirmados: portal ee062ef, buscas 7e9bd90 e PRO 40770b9.
- Inglês e espanhol: `node scripts/browser-locales.cjs` aprovado com progresso/checklist isolados, interface traduzida, grifos persistentes, recusa de importação entre idiomas, retomada, navegação, celular e leitura sem JS.
- `python3 scripts/validate.py`: 42 páginas, 144 tópicos (48 por idioma), IDs, links, manifestos e três kits aprovados.
- `python3 scripts/validate-locales.py`: 725 segmentos por idioma, nomes técnicos e comandos preservados, seleção de idioma e URLs canônicas aprovados.
- Bots PT/ES/EN: 11 cenários offline por edição (33 ao todo); JavaScript localizado com sintaxe válida.
- Revisão visual: início em inglês e espanhol, aula em espanhol, desktop/celular.
- Uma captura Chromium falhou na execução paralela; execução sequencial passou. Registro em LIMITES.md do hub wifi.

## Limites observados

Os testes do bot usam dados fictícios e não fazem chamadas reais ao Telegram. Não foi contratada nem alterada uma VPS. A instalação do Codex, autenticação e integração real pertencem às práticas do aluno. Progresso entre arquivos abertos diretamente por file:// depende do navegador; prefira servidor HTTP local.

## Capa

Skill capa-inema, engine local inemaimg, modelo flux2-klein. Cena: uma mesa profissional organizada com notebook, pastas, caderno, calendário e pequeno servidor. Saída: capa/capa.png; base: capa/base.png. Nenhuma geração de imagem acontece no navegador do aluno.

## Publicação

Push origin/main confirmado. GitHub Pages configurado em main /, build built sem erro e página inicial HTTP 200 em 20/09/2026.


Publicação 1.1.0: conteúdo ceb06d9 em origin/main; PT/ES/EN, último módulo ES/EN e kits ES/EN responderam HTTP 200. Cadastro internacional do portal: 108da90. Publicação do portal confirmada pelo push, sem consulta ao Vercel.
