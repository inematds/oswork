---
name: relatorio-semanal
description: Generate a draft weekly report when the user provides a sales CSV. Do not use it to send reports or handle credentials.
---

# Weekly Report

## Input
CSV provided by the user, with columns named produto and valor. Use only explicitly authorized sources.

## Procedure
1. Read README.md and the project instructions.
2. Check header, number of lines and values; explain invalid fields.
3. Calculate totals with the available calculation tool, without inventing missing entries.
4. Produce saidas/relatorio.md with sources, known total, valid records and pending items.
5. Verify the total against the sum of the records.
6. Report the verification and stop before sending or publishing.

## Behavioral tests
- Complete data: total consistent with the sum.
- Incomplete data: visible pending, without fabricated numbers.
- Out‑of‑scope request: explain the limitation; do not perform external actions.

## Installation of this example
Save as .agents/skills/relatorio-semanal/SKILL.md in the project, or ~/.agents/skills/relatorio-semanal/SKILL.md for personal use.
