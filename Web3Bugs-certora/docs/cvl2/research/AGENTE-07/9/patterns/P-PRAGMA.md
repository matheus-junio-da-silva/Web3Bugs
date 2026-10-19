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
