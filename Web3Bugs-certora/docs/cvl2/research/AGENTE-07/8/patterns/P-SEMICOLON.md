# P-SEMICOLON — Terminadores e using/import/use/invariant

**AGENTE-07 Fase 1 — Nota de padrão. Não é patch CVL2 nem prova de aplicabilidade automática.**

## Evidência
IDs: A2-SEMICOLON.
Referência: https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html

## Regra documental específica
CVL2 requer ; em using/import/use e invariants sem preserved/filtered associado.

## Plano conservador de mudança candidata
Localizar declaração literal e determinar se ela possui bloco associado; acrescentar terminador somente no derivado.

## Risco de alteração semântica
Aplicar ; automaticamente antes de preserved/filtered pode mudar parse ou ser inválido.

## Gate de promoção
1. Exigir linha de CVL original, original source path e contexto de import/target no dossier da property.
2. Associar evidência A1/A2 a esse caso específico e reconstruir qualquer target/ABI original necessário.
3. Distinguir erro original / dependência ausente / CLI / incompatibilidade CVL1→CVL2.
4. Não executar script de migração ou compilar nesta fase; exigir autorização antes de testar e demonstrar preservação semântica.
