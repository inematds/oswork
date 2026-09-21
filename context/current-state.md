# Estado atual — 2026-09-20

OSWork v2 implementado e validado: 14 páginas, 48 tópicos, oito laboratórios, kit e capa. Testes estáticos, navegador (13 grupos) e bot (11 cenários) aprovados. Publicado em https://inematds.github.io/oswork/ (HTTP 200). Push em origin/main confirmado.

OSWork v5 concluído e publicado em 21/09/2026, no repositório independente `../oswork-v5`. A descoberta pedagógica foi confirmada pelo usuário: profissionais 40+ iniciantes, gestora e professor como profissões-alvo, familiaridade baixa, resultado "organizar seu ambiente de IA", sessões de 20 a 25 minutos. Sete aulas, 150 minutos, formato formato-curso-v5. No ar em https://inematds.github.io/oswork-v5/ (HTTP 200) e cadastrado no portal, na busca e no PRO.


Ampliação 1.1.0: PT, ES e EN completos e validados — 42 páginas, 144 tópicos (48 por idioma), kits e interface traduzidos, navegação preservando aula e progresso isolado. Testes estáticos, navegador e 33 cenários dos bots aprovados. Publicado em https://inematds.github.io/oswork/ (PT), /es/ (ES) e /en/ (EN); três inícios, últimas aulas e kits com HTTP 200 em 20/09/2026. Commit de conteúdo ceb06d9.

Cadastro publicado no portal (PT ee062ef, EN/ES 108da90), busca (7e9bd90) e PRO (40770b9), com alterações concorrentes do Jev preservadas. Nenhum status de deploy Vercel foi consultado.

Edição 1.2.1 (21/09/2026): módulo 1.1 reescrito para explicar o que é uma LLM e por que não existe melhor modelo, apenas o adequado à tarefa; o tópico 2 passou a cobrir tipos de IA por função (texto, imagem, vídeo, classificação), centrais de acesso (OpenRouter, Kie) e classificadores emergentes (Jev). Cada módulo ganhou duas figuras explicativas em SVG, declaradas como dados em conteudo/modulos.py (FIGURES) e desenhadas por primitivas em build.py: grid, columns, flow, stack, tree e timeline. Rótulos de figura têm teto prático de 27 caracteres, válido também para ES e EN, porque wrap_diagrams reduz a fonte acima disso. Validadores, testes de navegador PT/ES/EN e bump 1.1.0 para 1.2.1 aplicados. Commits 3ea41da, 52d4e51, 3e2c2df.
