# P-VACUITY-W2W3 — AAVE Vault W2 e W3: denominador zero

**AGENTE-07 Fase 1 — Nota de padrão. Não é patch CVL2 nem prova de aplicabilidade automática.**

## Evidência
IDs: AXIOM-W1W2W3.
Referência: https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/docs/spec_catalog_project_8_math_review.md

## Regra documental específica
accrueYieldCheck.spec possui strict inequalities das axiomatizações mulDiv_g/rayDiv_g que falham em denominador zero.

## Plano conservador de mudança candidata
Vincular esta conclusão APENAS a accrueYieldCheck.spec, sob a presença literal daqueles axiomas e versão/target ainda não comprovados.

## Risco de alteração semântica
Não transferir este achado para changeInContractBalanceShouldCauseAccrual; não introduzir require denominador>0 arbitrariamente.

## Gate de promoção
1. Exigir linha de CVL original, original source path e contexto de import/target no dossier da property.
2. Associar evidência A1/A2 a esse caso específico e reconstruir qualquer target/ABI original necessário.
3. Distinguir erro original / dependência ausente / CLI / incompatibilidade CVL1→CVL2.
4. Não executar script de migração ou compilar nesta fase; exigir autorização antes de testar e demonstrar preservação semântica.
