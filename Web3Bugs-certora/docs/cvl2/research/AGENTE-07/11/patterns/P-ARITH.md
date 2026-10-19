# P-ARITH — Aritmética e casts

**AGENTE-07 Fase 1 — Nota de padrão. Não é patch CVL2 nem prova de aplicabilidade automática.**

## Evidência
IDs: A1-ARITH, A2-ARITH.
Referência: https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html

## Regra documental específica
Operações aritméticas em CVL2 retornam mathint; assert_ cast gera obrigação e require_ restringe estados.

## Plano conservador de mudança candidata
Confrontar expressão original, tipo e range real; preferir mathint para valores puramente CVL e analisar overflow antes de argumentos Solidity.

## Risco de alteração semântica
require_ pode esconder bugs por excluir contraexemplos; assert_ pode criá-los sem correspondência ao original.

## Gate de promoção
1. Exigir linha de CVL original, original source path e contexto de import/target no dossier da property.
2. Associar evidência A1/A2 a esse caso específico e reconstruir qualquer target/ABI original necessário.
3. Distinguir erro original / dependência ausente / CLI / incompatibilidade CVL1→CVL2.
4. Não executar script de migração ou compilar nesta fase; exigir autorização antes de testar e demonstrar preservação semântica.


## Evidence recheck — 2026-10-19
- Full-source verification was performed for all 16 extracted N.spec instances; refer to full_spec_audit.csv for exact file, byte SHA, line and candidate details.
- Simple token scanner occurrences in this project: 0 directly matching this pattern name (zero is not proof of absence; some pattern classifications are semantic rather than lexical).
- No generic Certora migration example is sufficient evidence for an automatic transformation; verify before/after for the actual original rule, ABI, receiver, summary, ghosts, storage and reverts. See official CVL2 migration and changes documentation.
