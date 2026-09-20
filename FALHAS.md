# Falhas corrigidas

| Data | O que quebrou | Menor correção | Prompt ou infra |
|---|---|---|---|
| 2026-09-20 | Texto visual dos medidores e do botão lido não acompanhava o estado | Usar atributos data-* esperados pelo motor; testar texto visível | prompt |
| 2026-09-20 | Jornada e aparência na navegação não recebiam cliques; painel continuava hidden | Delegar cliques no document e sincronizar hidden | infra |
| 2026-09-20 | Retomada e links de dúvidas não saíam da página atual | Resolver módulo pelo manifesto e preservar checkpoint fora das aulas | infra |
| 2026-09-20 | Importação não preservava campos adicionais nem rejeitava estruturas inválidas | Validar antes de alterar estado e persistir campos adicionais | infra |
