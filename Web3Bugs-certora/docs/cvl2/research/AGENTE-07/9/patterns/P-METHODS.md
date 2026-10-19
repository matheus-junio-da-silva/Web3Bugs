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
