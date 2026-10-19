# P-ORIGINAL-MAXINT — MAX_INT sem declaração original

**AGENTE-07 Fase 1 — Nota de padrão. Não é patch CVL2 nem prova de aplicabilidade automática.**

## Evidência
IDs: BENTOBOX-SCRIPTS, P20-N-TXT-23.
Referência: https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/docs/spec_catalog_project_20.md

## Regra documental específica
compoundStrategyAdditional.spec chama MAX_INT() sem definição CVL local ou import original demonstrado.

## Plano conservador de mudança candidata
Registrar como defeito/dependência original, distinto de CVL2. Buscar a origem exata no commit auditado, sem inserir definition ad hoc.

## Risco de alteração semântica
Inventar constante torna novo modelo divergente da spec auditada; linha de prova não está comprovada.

## Gate de promoção
1. Exigir linha de CVL original, original source path e contexto de import/target no dossier da property.
2. Associar evidência A1/A2 a esse caso específico e reconstruir qualquer target/ABI original necessário.
3. Distinguir erro original / dependência ausente / CLI / incompatibilidade CVL1→CVL2.
4. Não executar script de migração ou compilar nesta fase; exigir autorização antes de testar e demonstrar preservação semântica.


## Evidence recheck — 2026-10-19
- Full-source verification was performed for all 37 extracted N.spec instances; refer to full_spec_audit.csv for exact file, byte SHA, line and candidate details.
- Simple token scanner occurrences in this project: 0 directly matching this pattern name (zero is not proof of absence; some pattern classifications are semantic rather than lexical).
- No generic Certora migration example is sufficient evidence for an automatic transformation; verify before/after for the actual original rule, ABI, receiver, summary, ghosts, storage and reverts. See official CVL2 migration and changes documentation.
