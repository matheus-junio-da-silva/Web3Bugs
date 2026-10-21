# P-METHODS — Declarações em methods

**AGENTE-07 Fase 1 — Nota de padrão. Não é patch CVL2 nem prova de aplicabilidade automática.**

## Evidência
IDs: A1-METHODS, A2-METHODS.
Referência: https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html

## Regra documental específica
CVL2 exige function, ; e annotation internal/external; public Solidity pode ter entradas interna e externa diferentes.

## Plano conservador de mudança candidata
Citar a entrada CVL real, confrontar Solidity ABI/harness e preservar receiver. Candidate adicionar function e ;, mas visibility/target só depois do fechamento.

## Risco de alteração semântica
CVL1 pode ignorar método inexistente; CVL2 usa optional expresso. DISPATCHER e summaries afetam universo de calls.

## Gate de promoção
1. Exigir linha de CVL original, original source path e contexto de import/target no dossier da property.
2. Associar evidência A1/A2 a esse caso específico e reconstruir qualquer target/ABI original necessário.
3. Distinguir erro original / dependência ausente / CLI / incompatibilidade CVL1→CVL2.
4. Não executar script de migração ou compilar nesta fase; exigir autorização antes de testar e demonstrar preservação semântica.


## Evidence recheck — 2026-10-19
- Full-source verification was performed for all 42 extracted N.spec instances; refer to full_spec_audit.csv for exact file, byte SHA, line and candidate details.
- Specific source scanner occurrences in this project: 408 for category METHOD_ENTRY; not distinct rule count, some repeated shared methods (zero is not proof of absence; some pattern classifications are semantic rather than lexical).
- No generic Certora migration example is sufficient evidence for an automatic transformation; verify before/after for the actual original rule, ABI, receiver, summary, ghosts, storage and reverts. See official CVL2 migration and changes documentation.
