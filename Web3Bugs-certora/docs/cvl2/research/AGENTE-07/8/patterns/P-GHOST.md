# P-GHOST — Ghosts, axioms, hooks e storage

**AGENTE-07 Fase 1 — Nota de padrão. Não é patch CVL2 nem prova de aplicabilidade automática.**

## Evidência
IDs: A2-GHOST, A2-HOOK.
Referência: https://docs.certora.com/en/latest/docs/cvl/ghosts.html

## Regra documental específica
Assunções axiomáticas e hooks restringem estados e relações de armazenamento observáveis.

## Plano conservador de mudança candidata
Inspecionar axiom, hook, init_state, armazenamento, receiver e mudanças derivadas; não consertar sem intenção documental autorizada.

## Risco de alteração semântica
Axiomas inconsistentes podem resultar prova vacuamente verdadeira; hooks mal endereçados podem falsificar o modelo.

## Gate de promoção
1. Exigir linha de CVL original, original source path e contexto de import/target no dossier da property.
2. Associar evidência A1/A2 a esse caso específico e reconstruir qualquer target/ABI original necessário.
3. Distinguir erro original / dependência ausente / CLI / incompatibilidade CVL1→CVL2.
4. Não executar script de migração ou compilar nesta fase; exigir autorização antes de testar e demonstrar preservação semântica.
