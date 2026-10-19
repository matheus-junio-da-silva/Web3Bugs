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


## Evidence recheck — 2026-10-19
- Full-source verification was performed for all 42 extracted N.spec instances; refer to full_spec_audit.csv for exact file, byte SHA, line and candidate details.
- Specific source scanner occurrences in this project: 1 for category W2_W3_ZERO_DENOMINATOR_GLOBAL_AXIOMS; not distinct rule count, some repeated shared methods (zero is not proof of absence; some pattern classifications are semantic rather than lexical).
- No generic Certora migration example is sufficient evidence for an automatic transformation; verify before/after for the actual original rule, ABI, receiver, summary, ghosts, storage and reverts. See official CVL2 migration and changes documentation.
