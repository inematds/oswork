# OSWork — edição v2

Curso estático INEMA.CLUB sobre IA como sistema de trabalho.
- Conta e autoria: inematds <inematds@gmail.com>, author e committer.
- Edição v2 neste repositório; edição v5 em ../oswork-v5, repositório independente.
- Leia context/overview.md, context/current-state.md e tasks/current.md.
- Conteúdo autoral: conteudo/modulos.py; gerador: scripts/build.py.
- Regere PT com python3 scripts/build.py e idiomas com python3 scripts/build-locales.py. Traduções completas ficam em i18n/, páginas em es/ e en/.
- Se mudar learn.js/site.js, atualize índices com node scripts/extract-js-strings.cjs antes de gerar idiomas.
- Progresso/notas/checklists são separados por idioma; preferências visuais são compartilhadas.
- Verifique com python3 scripts/validate.py, python3 scripts/validate-locales.py, node scripts/browser-test.cjs e node scripts/browser-locales.cjs. Execute autoteste dos bots PT/ES/EN.
- Nunca publicar credenciais. Exemplos são fictícios.
- Publicação por git, GitHub Pages main /; não usar Vercel.
