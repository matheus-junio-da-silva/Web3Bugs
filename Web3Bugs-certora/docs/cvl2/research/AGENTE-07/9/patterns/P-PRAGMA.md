# P-PRAGMA — Remoção de pragma

**AGENTE-07 Fase 1 — Nota de padrão. Não é patch CVL2 nem prova de aplicabilidade automática.**

## Evidência
IDs: A2-PRAGMA.
Referência: https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html

## Regra documental específica
CVL2 remove diretivas pragma de CVL1.

## Plano conservador de mudança candidata
Identificar pragma original ativo e remover apenas da cópia CVL2 derivada; jamais da fonte CVL histórica.

## Risco de alteração semântica
Não tratar comentários contendo pragma como diretivas; versão original preservada no histórico.

## Gate de promoção
1. Exigir linha de CVL original, original source path e contexto de import/target no dossier da property.
2. Associar evidência A1/A2 a esse caso específico e reconstruir qualquer target/ABI original necessário.
3. Distinguir erro original / dependência ausente / CLI / incompatibilidade CVL1→CVL2.
4. Não executar script de migração ou compilar nesta fase; exigir autorização antes de testar e demonstrar preservação semântica.


## Evidence recheck — 2026-10-19
- Full-source verification was performed for all 61 extracted N.spec instances; refer to full_spec_audit.csv for exact file, byte SHA, line and candidate details.
- Simple token scanner occurrences in this project: 33 directly matching this pattern name (zero is not proof of absence; some pattern classifications are semantic rather than lexical).
- No generic Certora migration example is sufficient evidence for an automatic transformation; verify before/after for the actual original rule, ABI, receiver, summary, ghosts, storage and reverts. See official CVL2 migration and changes documentation.
