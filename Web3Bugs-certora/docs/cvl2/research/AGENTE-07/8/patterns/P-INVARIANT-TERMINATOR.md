# P-INVARIANT-TERMINATOR — Invariant terminator; candidate a auditar

**AGENTE-07 Fase 1 — Nota de padrão. Não é patch CVL2 nem prova de aplicabilidade automática.**

## Evidência
IDs: A2-SEMICOLON.
Referência: https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html

## Regra documental específica
Regra explícita de ; no final de invariant, exceto quando segue preserved/filtered.

## Plano conservador de mudança candidata
Auditar individualmente linhas originais de invariant e preserved; nenhum dossiê ganha este ID por inferência apenas da palavra invariant.

## Risco de alteração semântica
É um lembrete de checklist, não afirmação de incompatibilidade por propriedade.

## Gate de promoção
1. Exigir linha de CVL original, original source path e contexto de import/target no dossier da property.
2. Associar evidência A1/A2 a esse caso específico e reconstruir qualquer target/ABI original necessário.
3. Distinguir erro original / dependência ausente / CLI / incompatibilidade CVL1→CVL2.
4. Não executar script de migração ou compilar nesta fase; exigir autorização antes de testar e demonstrar preservação semântica.
