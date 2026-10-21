# Upstream checks — AGENTE-07 / Project 8 — AAVE Vault

Fase 1 documental, 2026-10-19. Consultas GET feitas via conexão GitHub; nunca executado Prover/compilador.

| Evidência | Repositório | Commit | Resultado | Referência |
|---|---|---|---|---|
| Historical exact audit commit | NOT_PINNED_IN_EVIDENCE | NOT_PROVEN | Nenhum commit de execução do Prover inferido do PDF/catálogo | https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/docs/spec_catalog_project_8.md |

## Limites e impacto
Axiomas W1/W2/W3 têm contradições aritméticas demonstradas por revisão independente existente, mas ausência de commit e flags da execução não prova a exposição do Prover histórico. Não classificar RECONSTRUCTED.

**Não há blob SHA comprovadamente correspondente ao código e import closure do Prover histórico para todos os casos.** Os dossiers mantêm `UNRESOLVED_CANDIDATE` onde falta essa correspondência.

## Historical dependency follow-up — 2026-10-19
Original P8 axioms were preserved byte-for-byte. The independent mathematical witness documented in docs/spec_catalog_project_8_math_review.md and the full-source inspection pinpoints:
- W1: 22 instance extractions IDs 14-35, from fees_LEQ_ATokenBal.spec, lastVaultBal_LEQ_ATokenBalThis.spec and positiveSupply_imply_positiveAssets.spec, with globally scoped rayMul ghost axioms. Witness x=1,y=0 violates simultaneous strict lower/upper arithmetic bounds.
- W2 + W3: one extraction ID 1, accrueYieldCheck.spec. The mulDiv strict axiom with denominator=0 forces 0<0; similarly rayDiv with y=0. Both are ambient universal axioms even when target rule does not call the ghost.
- Other 19 instances: neither of these specific contradictions identified, NOT certified nonvacuous or safe.
- A result VERIFIED reported historically is not equivalent to sound proof under the exact extracted model or a replay. Status remains untouched. Do not insert denominator !=0 guards, alter quantifier range, remove axioms or constrain sender/env for convenience.
- The full N.spec and the source range for each selected property are logged in full_spec_audit.csv and in the individual property, with exact source bytes.
