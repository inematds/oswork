# OSWork — IA como sistema de trabalho

Curso completo no formato INEMA v2. Quatro trilhas, oito módulos, 48 tópicos e kit de exercícios.

- Português: https://inematds.github.io/oswork/
- Español: https://inematds.github.io/oswork/es/
- English: https://inematds.github.io/oswork/en/
- Edição v5 planejada em repositório separado `inematds/oswork-v5`; descoberta pedagógica pendente.
- Versão do projeto: 1.1.0
- Fontes revisadas: 20/09/2026, listadas em FONTES.md.

## Percurso

1. Modelos e critérios de escolha.
2. Chat, Work e Desktop.
3. Terminal e Codex.
4. Pastas, Markdown e segredos.
5. AGENTS.md, Skills e memória.
6. Git e GitHub.
7. Telegram como interface.
8. VPS, supervisão e recuperação.

## Estudar localmente

Abra index.html ou execute `python3 -m http.server 8080` e acesse http://localhost:8080. O uso por HTTP mantém uma origem comum para progresso entre páginas. Em file:// o armazenamento entre páginas varia por navegador. Não há backend, cadastro, biblioteca de interface remota nem chamadas de IA durante o estudo.

## Editar

Conteúdo em `conteudo/modulos.py`, geração em `scripts/build.py`. Depois de editar, execute:

```bash
python3 scripts/build.py
python3 scripts/build-locales.py
python3 scripts/validate.py
python3 materiais/bot/bot.py --self-test
```

O teste de navegador requer Playwright/Chromium e um servidor local. Configure `BASE_URL` e, se necessário, `PLAYWRIGHT_PATH` antes de `node scripts/browser-test.cjs`. Evidências temporárias ficam em `.verificacao/`, ignorada pelo Git.

## Traduções v2

As três edições possuem as mesmas 4 trilhas, 8 módulos e 48 tópicos. O seletor de idioma mantém a aula atual. Progresso, notas, dúvidas e checklist são separados por idioma; as preferências visuais são compartilhadas. Uma exportação de jornada só pode ser importada no mesmo idioma.

`i18n/es.json` e `i18n/en.json` guardam traduções revisáveis, sem chamadas externas ao gerar páginas. `scripts/build-locales.py` requer BeautifulSoup (`python3 -m pip install beautifulsoup4`). Para alterações de conteúdo, extraia o catálogo com `python3 scripts/localization.py`, atualize os dicionários e gere novamente. A ferramenta opcional `scripts/translate.py es en` usa Groq, com chave carregada em runtime dos arquivos de configuração locais indicados nas instruções globais. Não é necessária para estudar ou publicar traduções já salvas. Interface e bot têm dicionários separados em `i18n/`. Se alterar os arquivos JS originais, atualize os índices com `node scripts/extract-js-strings.cjs` (requer TypeScript local, ou `TYPESCRIPT_PATH` apontando para a instalação).

Execute também `node scripts/browser-locales.cjs` para verificar os idiomas.

## Materiais

`materiais/oswork-kit.zip` contém modelos e um bot de consulta determinístico. O autoteste não usa credenciais nem rede. A conexão real Telegram e a implantação em uma VPS pertencem ao laboratório do aluno e devem ser verificadas no seu ambiente. Não há IA conectada ao bot base.

## Aprendizagem

Progresso por tópico, dúvidas, grifos/notas, exportação/importação e preferências persistem no navegador. O modo efêmero mantém a leitura quando armazenamento não está disponível. Exporte a jornada antes de limpar dados do navegador.

## Publicação

GitHub Pages, branch main e pasta raiz. Autoria: inematds <inematds@gmail.com>. As edições v2 e v5 são repositórios independentes.
