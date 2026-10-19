# AGENTE-05 — P19 Origin OUSD / Phase 1 research

**HEADs confirmed 2026-10-19:** Web3Bugs `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3` and PropertyGPT `687f654c679ed45ab127b7949e2a29c8f5e491b9`.

**Inventory:** 37 unique cataloged examples (2 complete, 35 incomplete); 37 original label relations, deduplicated by `(project_id,status,example_id)` not by rule name.

**Sources:** `Web3Bugs-certora/contracts/19/`, `Web3Bugs-certora/docs/spec_catalog_project_19.md`, `resources/19/OriginFeb2021.pdf`, `PropertyGPT/certora_projects/ousd` at 687f654c679ed45ab127b7949e2a29c8f5e491b9. PDF reviewed revision claim `5c702edbefb451287805918c3275535c11654074` requires per-instance verification.

**Critical context:** Unvendored historical @openzeppelin packages; scripts alter harness state/caps and target; 36 declarations become 37 target-specific instances; privilegedOperation must not be inferred as ACL.

**Documents:** `properties.csv` per-key inventory; `properties/{complete,incomplete}/N.md` individual analysis; `patterns/methods-quantifiers-type-system.md` source-guided patterns; `evidence_register.csv` source URLs and blob IDs; `recovery_manifest.csv` only incomplete dependencies; `QA_REPORT.md` reconciliations.

**SEM ALTERAÇÕES EM SPECS; SEM COMPILAÇÃO CVL2; SEM PROVER; SEM TESTE CVL1.** Candidate buckets never represent compiled or verified specs.
