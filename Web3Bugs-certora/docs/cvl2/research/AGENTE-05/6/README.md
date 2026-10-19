# AGENTE-05 — P6 AAVE Static aToken / Phase 1 research

**HEADs confirmed 2026-10-19:** Web3Bugs `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3` and PropertyGPT `687f654c679ed45ab127b7949e2a29c8f5e491b9`.

**Inventory:** 32 unique cataloged examples (0 complete, 32 incomplete); 33 original label relations, deduplicated by `(project_id,status,example_id)` not by rule name.

**Sources:** `Web3Bugs-certora/contracts/6/`, `Web3Bugs-certora/docs/spec_catalog_project_6.md`, `resources/6/Formal_Verification_Report_staticAToken.pdf`, `PropertyGPT/certora_projects/aave_static_token` at 687f654c679ed45ab127b7949e2a29c8f5e491b9. PDF reviewed revision claim `ac92951 (PDF abbreviation; full SHA not yet evidenced)` requires per-instance verification.

**Critical context:** Exact StaticATokenLMHarness and verify scripts unavailable, external ERC20/AToken/RewardsController dependency graph incomplete. Supplied StaticATokenLM.sol matches 13a004738c533f11710400c1757b9570ef1e0466 rather than later report revision ac92951. Preserve 32 source instances vs 24 PropertyGPT CSV.

**Documents:** `properties.csv` per-key inventory; `properties/{complete,incomplete}/N.md` individual analysis; `patterns/methods-quantifiers-type-system.md` source-guided patterns; `evidence_register.csv` source URLs and blob IDs; `recovery_manifest.csv` only incomplete dependencies; `QA_REPORT.md` reconciliations.

**SEM ALTERAÇÕES EM SPECS; SEM COMPILAÇÃO CVL2; SEM PROVER; SEM TESTE CVL1.** Candidate buckets never represent compiled or verified specs.
