# AGENTE-05 — P7 AAVE V3 / Phase 1 research

**HEADs confirmed 2026-10-19:** Web3Bugs `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3` and PropertyGPT `687f654c679ed45ab127b7949e2a29c8f5e491b9`.

**Inventory:** 74 unique cataloged examples (46 complete, 28 incomplete); 74 original label relations, deduplicated by `(project_id,status,example_id)` not by rule name.

**Sources:** `Web3Bugs-certora/contracts/7/`, `Web3Bugs-certora/docs/spec_catalog_project_7.md`, `resources/7/AaveV3Jan2022-1.pdf`, `PropertyGPT/certora_projects/aave_v3` at 687f654c679ed45ab127b7949e2a29c8f5e491b9. PDF reviewed revision claim `a87d546 (PDF abbreviation)` requires per-instance verification.

**Critical context:** 74 rule/target instances distinct from PDF aggregate; non-vendored mocks and helpers for 28 incomplete. Individual 18 VERIFIED vs 56 NOT_STATED cannot be replaced by aggregated claims.

**Documents:** `properties.csv` per-key inventory; `properties/{complete,incomplete}/N.md` individual analysis; `patterns/methods-quantifiers-type-system.md` source-guided patterns; `evidence_register.csv` source URLs and blob IDs; `recovery_manifest.csv` only incomplete dependencies; `QA_REPORT.md` reconciliations.

**SEM ALTERAÇÕES EM SPECS; SEM COMPILAÇÃO CVL2; SEM PROVER; SEM TESTE CVL1.** Candidate buckets never represent compiled or verified specs.
