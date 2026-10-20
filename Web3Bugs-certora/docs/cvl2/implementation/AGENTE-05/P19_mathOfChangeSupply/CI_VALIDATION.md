# GitHub Actions validation — PR #46 (2026-10-19)

## Audited commit and environment

- PR: https://github.com/matheus-junio-da-silva/Web3Bugs/pull/46
- Head at checks: `82674b18e8c54aacf8d41166e7db5f3fe1505561`
- Base: `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`
- These checks executed on GitHub-hosted Actions runners, not on the unavailable local/remote AGENTE-05 machine.
- CI validates catalog/integrity and Git whitespace; **not CVL2 compilation or semantic equivalence**.

## Three official validators — independent CI execution

[Project 24 full catalog validation, run 39333784639](https://github.com/matheus-junio-da-silva/Web3Bugs/actions/runs/39333784639), job `118338099471`:

| Command/step | Actual exit/status | Console |
| --- | --- | --- |
| `python scripts/check_specs.py .` | exit 0 | `Check passed! 1386 spec examples and 1390 Bug Label relationships are structurally consistent.` |
| `python scripts/check_contests_csv.py .` | exit 0 | PASS |
| `python scripts/check_contracts.py .` | exit 0 | PASS |
| `git -c core.whitespace=cr-at-eol diff --check origin/main...HEAD` | **exit 2** | ten `trailing whitespace` diagnostics (listed below) |

The CI composite step ultimately failed (exit 1) because the Git diff check returned 2, **not** because any of the three official catalog validators failed.

## Exact Git whitespace findings

```text
Web3Bugs-certora/results/cvl2/02_unresolved/19/1.spec:4: trailing whitespace.
Web3Bugs-certora/results/cvl2/02_unresolved/19/1.spec:7: trailing whitespace.
Web3Bugs-certora/results/cvl2/02_unresolved/19/1.spec:17: trailing whitespace.
Web3Bugs-certora/results/cvl2/02_unresolved/19/1.spec:20: trailing whitespace.
Web3Bugs-certora/results/cvl2/02_unresolved/19/1.spec:22: trailing whitespace.
Web3Bugs-certora/results/cvl2/02_unresolved/19/2.spec:4: trailing whitespace.
Web3Bugs-certora/results/cvl2/02_unresolved/19/2.spec:7: trailing whitespace.
Web3Bugs-certora/results/cvl2/02_unresolved/19/2.spec:17: trailing whitespace.
Web3Bugs-certora/results/cvl2/02_unresolved/19/2.spec:20: trailing whitespace.
Web3Bugs-certora/results/cvl2/02_unresolved/19/2.spec:22: trailing whitespace.
```

Each trailing-space line is preserved from the historic original. The exact SHA-256 of each derived spec matches the coordinator's reviewed candidate; removing the whitespace would violate the single-change, byte-faithful authorization.

**Decision needed:** coordinator must explicitly resolve conflict between strict whitespace gate and preservation-of-every-other-byte mandate (e.g., authorize a *narrow path-scoped Git whitespace attribute* as a separate change, or accept the documented CI waiver). **No additional file or edit was made to bypass the check.** A global whitespace-policy change is not proposed.

## Principal integrity workflow

[validate, run 39333784635](https://github.com/matheus-junio-da-silva/Web3Bugs/actions/runs/39333784635), job `118338099297`: **success**.

- `check_contests_csv`: success.
- `check_contracts`: success.
- `check_git`: success.

This run does **not** erase the failure of the independent Project 24 whitespace check.

## Status of compilation and semantics

Only the independent coordinator's *previous* CVL2 compilation-only checks (PR #44) have candidate exit 0; AGENTE-05 did **not** rerun the Certora CLI in this session. The absence of fresh compiler logs/durations is intentionally recorded, not concealed.

**Current classification: 02_unresolved. No Prover, no CVL1, no merge.**

AGENTE-05 — FASE 2 / IMPLEMENTAÇÃO EXPERIMENTAL P19.


## Fechamento independente do gate de whitespace — coordenador (2026-10-19)

**Os resultados EXIT 2 anteriores acima são históricos e permanecem documentados.** O coordenador adicionou em commit `b361c37af657acecb2e7878de64183e267f812b3` um único `.gitattributes` dentro de `results/cvl2/02_unresolved/19/`, limitado estritamente a `/1.spec` e `/2.spec`:

```gitattributes
/1.spec whitespace=-blank-at-eol,blank-at-eof,space-before-tab,cr-at-eol
/2.spec whitespace=-blank-at-eol,blank-at-eof,space-before-tab,cr-at-eol
```

A regra ignora **somente trailing whitespace histórico** nesses dois arquivos, mantendo os checks `blank-at-eof` e `space-before-tab`, sem alterar política fora dessas duas paths. A sintaxe foi testada isoladamente num repositório Git descartável antes da modificação do PR.

Evidência CI depois desse commit:
- [Project 24 full catalog validation — run 39335229214](https://github.com/matheus-junio-da-silva/Web3Bugs/actions/runs/39335229214): **SUCCESS**, inclusive o step `Three official validators and exact Git whitespace command`.
- [validate — run 39335229210](https://github.com/matheus-junio-da-silva/Web3Bugs/actions/runs/39335229210): **SUCCESS**.

Verificação independente pelo coordenador, buscando as fontes no SHA original e derivadas no SHA pós-atributos: para cada Example ID 1/2, a string integral derivada corresponde EXATAMENTE à substituição única `divPrecisely(uint x, uint y)` → `divPrecisely(mathint x, mathint y)`; os dois `assert` finais permanecem byte-idênticos e distintos, com zero outras mudanças textuais.

Este resultado **resolve o gate de CI/whitespace, NÃO o gate de equivalência**. O compilador CVL2 com `--compilation_steps_only` havia retornado exit 0 para cada variante em experimento independente anterior; não houve novo Prover/CVL1/compilação neste commit. Os riscos de `RCPT=0` e semântica de divisão por zero permanecem abertos, bem como ausência de reprodução do engine CVL1. **Os dois exemplos permanecem em `02_unresolved` e o PR DRAFT, sem merge.**
