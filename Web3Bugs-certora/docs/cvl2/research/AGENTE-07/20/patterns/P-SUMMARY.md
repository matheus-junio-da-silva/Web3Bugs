# P-SUMMARY — Receiver e escopo das summaries

**AGENTE-07 Fase 1 — Nota de padrão. Não é patch CVL2 nem prova de aplicabilidade automática.**

## Evidência
IDs: A1-METHODS, A2-SUMMARY.
Referência: https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html

## Regra documental específica
CVL1 resume a assinatura em todos contratos; em CVL2 o escopo é currentContract por padrão e _ exige regra de wildcard específica.

## Plano conservador de mudança candidata
Identificar entrada com => no CVL, contrato definidor no Solidity, hierarquia de herança, filtros, uso via delegatecall/external/internal. Não criar _ indiscriminadamente.

## Risco de alteração semântica
Narrowing receiver pode remover ou produzir contraexemplos; wildcard impossibilita algumas combinações com envfree, optional ou return type.

## Gate de promoção
1. Exigir linha de CVL original, original source path e contexto de import/target no dossier da property.
2. Associar evidência A1/A2 a esse caso específico e reconstruir qualquer target/ABI original necessário.
3. Distinguir erro original / dependência ausente / CLI / incompatibilidade CVL1→CVL2.
4. Não executar script de migração ou compilar nesta fase; exigir autorização antes de testar e demonstrar preservação semântica.


## Evidence recheck — 2026-10-19
- Full-source verification was performed for all 37 extracted N.spec instances; refer to full_spec_audit.csv for exact file, byte SHA, line and candidate details.
- Specific source scanner occurrences in this project: 58 for category SUMMARY_RECEIVER; not distinct rule count, some repeated shared methods (zero is not proof of absence; some pattern classifications are semantic rather than lexical).
- No generic Certora migration example is sufficient evidence for an automatic transformation; verify before/after for the actual original rule, ABI, receiver, summary, ghosts, storage and reverts. See official CVL2 migration and changes documentation.
