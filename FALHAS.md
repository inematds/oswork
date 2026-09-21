# Falhas corrigidas


| Data | O que quebrou | Menor correção | Prompt ou infra |
|---|---|---|---|
| 2026-09-21 | pkill -f "http.server 33541" matou o próprio shell do agente (exit 144) | Guardar o PID ao subir o servidor e encerrar por PID | infra
| 2026-09-20 | Validação rejeitou tradução curta válida FERRAMENTAS → TOOLS | Aplicar limite de encurtamento apenas a blocos longos | prompt |
| 2026-09-20 | Tradução alterou nomes de arquivos citados no texto | Corrigir dicionário e validar preservação dos nomes e comandos | prompt |
| 2026-09-20 | Retomada sumia ao recarregar logo após marcar lido | Persistir checkpoint imediatamente, sem timer cancelado na navegação | infra |
| 2026-09-20 | Quebra de linha inseria espaço em nomes e flags hifenizados | Desativar break_on_hyphens na formatação do HTML | prompt |
| 2026-09-20 | Diagramas cortavam títulos no meio da palavra | Preservar título completo e quebrar linhas SVG na geração multilíngue | prompt |
| 2026-09-20 | Tradução devolveu um ID hash truncado | Enviar IDs numéricos curtos e validar conjunto antes de salvar | prompt |
| 2026-09-20 | Texto visual dos medidores e do botão lido não acompanhava o estado | Usar atributos data-* esperados pelo motor; testar texto visível | prompt |
| 2026-09-20 | Jornada e aparência na navegação não recebiam cliques; painel continuava hidden | Delegar cliques no document e sincronizar hidden | infra |
| 2026-09-20 | Retomada e links de dúvidas não saíam da página atual | Resolver módulo pelo manifesto e preservar checkpoint fora das aulas | infra |
| 2026-09-20 | Importação não preservava campos adicionais nem rejeitava estruturas inválidas | Validar antes de alterar estado e persistir campos adicionais | infra |
