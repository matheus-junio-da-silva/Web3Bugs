# P-LEGACY — invoke, sinvoke e static assertions

**AGENTE-07 Fase 1 — Nota de padrão. Não é patch CVL2 nem prova de aplicabilidade automática.**

## Evidência
IDs: A1-MIGRATION, A2-LEGACY.
Referência: https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html

## Regra documental específica
Guia oficial cita trocas de sinvoke, invoke, static_assert e static_require, mas cada uma tem semântica de revert e caminhos diferentes.

## Plano conservador de mudança candidata
Registrar literal CVL1 e candidate f(...) ou f@withrevert(...) conforme tipo de chamada; avaliar revert e post-state em relação ao original.

## Risco de alteração semântica
Substituição por chamada direta errada pode eliminar comportamento de revert e contraexemplos.

## Gate de promoção
1. Exigir linha de CVL original, original source path e contexto de import/target no dossier da property.
2. Associar evidência A1/A2 a esse caso específico e reconstruir qualquer target/ABI original necessário.
3. Distinguir erro original / dependência ausente / CLI / incompatibilidade CVL1→CVL2.
4. Não executar script de migração ou compilar nesta fase; exigir autorização antes de testar e demonstrar preservação semântica.
