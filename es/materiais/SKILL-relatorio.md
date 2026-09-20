---
name: relatorio-semanal
description: Generar borrador de informe semanal cuando el usuario proporcione un CSV de ventas. No usar para enviar informes ni manejar credenciales.
---

# Informe semanal

## Entrada
CSV indicado por el usuario, que contiene las columnas llamadas produto y valor. Use solo fuentes explícitamente autorizadas.

## Procedimiento
1. Lea README.md y las instrucciones del proyecto.
2. Verifique encabezado, número de líneas y valores; explique campos inválidos.
3. Calcule los totales con la herramienta de cálculo disponible, sin inventar ausencias.
4. Produzca saidas/relatorio.md con fuentes, total conocido, registros válidos y pendientes.
5. Verifique el total contra la suma de los registros.
6. Informe la verificación y deténgase antes de enviar o publicar.

## Pruebas de comportamiento
- Datos completos: total consistente con la suma.
- Datos incompletos: pendiente visible, sin números fabricados.
- Solicitud fuera del alcance: explique la limitación; no ejecute acciones externas.

## Instalación de este ejemplo
Guarde como .agents/skills/relatorio-semanal/SKILL.md en el proyecto, o ~/.agents/skills/relatorio-semanal/SKILL.md para uso personal.
