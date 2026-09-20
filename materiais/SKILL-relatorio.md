---
name: relatorio-semanal
description: Gerar rascunho de relatório semanal quando o usuário fornecer um CSV de vendas. Não usar para enviar relatórios ou tratar credenciais.
---

# Relatório semanal

## Entrada
CSV indicado pelo usuário, contendo produto e valor. Use apenas fontes explicitamente autorizadas.

## Procedimento
1. Leia README.md e as instruções do projeto.
2. Confira cabeçalho, número de linhas e valores; explique campos inválidos.
3. Calcule os totais com ferramenta de cálculo disponível, sem inventar ausências.
4. Produza saidas/relatorio.md com fontes, total conhecido, registros válidos e pendências.
5. Confira o total contra a soma dos registros.
6. Relate a verificação e pare antes de enviar ou publicar.

## Testes de comportamento
- Dados completos: total consistente com a soma.
- Dados incompletos: pendência visível, sem números fabricados.
- Pedido fora do escopo: explique a limitação; não execute ações externas.

## Instalação deste exemplo
Salve como .agents/skills/relatorio-semanal/SKILL.md no projeto, ou ~/.agents/skills/relatorio-semanal/SKILL.md para uso pessoal.
