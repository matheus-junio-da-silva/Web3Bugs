# AGENTE-06 — P22 source version with six exact matches

- The historical PDF in `reports/22.md` states verification work from September 22 to October 25, 2021 but does not pin a code commit SHA.
- Source repository cited in report: [Popsicle-Finance/PopsicleV3Optimizer](https://github.com/Popsicle-Finance/PopsicleV3Optimizer). Archived `certora` branch HEAD is [3cb9cb7279a3fb1790b55251a029bb3065606dc8](https://github.com/Popsicle-Finance/PopsicleV3Optimizer/commit/3cb9cb7279a3fb1790b55251a029bb3065606dc8), dated November 4, 2021, message "fixes based on the recently submited final version".
- Because this commit postdates the verification window described by the report, **it is NOT labeled the audited commit**. Source_commit_audited remains NOT_CONFIRMED.

## Confirmed Git blob identities

| File | Source + archive blob SHA |
|---|---|
| `spec/FullMathWrapper.spec` | `4add6fed2e9c62788e35b067d626662e3b90bb23` — exact match |
| `spec/PoolActions.spec` | `e3b1fdaee2c09f8f49f878b21de8cb3131dda756` — exact match |
| `spec/PopsicleV3Optimizer.spec` | `ef68e8556e07900d7f1f20e35fbbbefec7953484` — exact match |
| `spec/sanity.spec` | `655b96a099cbc9f5d8b25ea7a1ecbe142ed89cc2` — exact match |
| `spec/scripts/verifyPopsicleV3Optimizer.sh` | `9b25cf5a8aa340593a125c1eb8ebfaaa6e87f731` — exact match |
| `contracts/popsicle-v3-optimizer/PopsicleV3Optimizer.sol` | `d833d4dc0b66b5e066a2973c6c4b1b3e507eca40` — exact match |

## Runner scope
- `spec/scripts/verifyPopsicleV3Optimizer.sh` matches byte-for-byte and selects ONLY `PopsicleV3Optimizer:spec/PopsicleV3Optimizer.spec` with `--rule $1`, `solc7.6`, symbolic pool and token linkage, optimistic loop and one unrolled iteration.
- There is no evidence this command executed PoolActions, FullMathWrapper or sanity specs; cannot generalize the reported proofs.
- P22 incomplete PoolActions #4–5 still reference unavailable `totalSupply()` ABI getter in a wrapper with a private field. Do not create the getter merely to compile.

**This establishes archival source provenance only. No CVL2, Prover or CVL1 execution; no historical specs changed.**
