# AGENTE-01 — Project 10 Furucombo, CVL1→CVL2 research (FASE 1)

Scope is exactly Project ID **10**; source index `Web3Bugs-certora/results/spec/spec_buglabel.csv` at **2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3**, PropertyGPT at **687f654c679ed45ab127b7949e2a29c8f5e491b9**. Audited upstream: **dinngo/furucombo-contract @ c90dec1046e5e26edf70f985dd86381403912482** (reported in April 2021 Certora report, preserved as `resources/10/FurucomboMay2021.pdf`; transcript `reports/10.md`). Research date 2026-10-19.

**Reconciled:** **266 distinct (Project ID, Status, Example ID) examples**, 2 complete and 264 incomplete, 34 CVL active declarations represented by 31 distinct property names (several target-aware duplications); 23 historical handler targets. 138 additional incomplete source/handler contexts for report checks #27–32 were catalogued; they are **not** 138 individually attested 2021 Prover jobs. A result `NOT_STATED` remains historical unknown, not CVL2 failure.

## Key provenance finding

The report-pinned SHA is available in the archived/renamed upstream repo `dinngo/furucombo-contract`; audit source `package.json` pins Solidity **0.6.12** and `@openzeppelin/contracts 3.3.0`. The preserved modern snapshot uses different Solidity blobs in **22/22** distinct target Solidity source paths (see recovery_manifest). `specs/proxy.spec` and `specs/registry.spec` differ between audited commit and snapshot. Proxy rule names `nonExecutableWhenProxyIsBanned` and `nonExecutableWithInitializedSender` are absent at the exact audited SHA: no 2021 verified-result attribution is defensible for these two later rule names. Other proxy rule bodies also differ.

Recovered upstream Git blobs make targeted historical reconstruction *possible* but do not establish imported npm code or a byte-identical 2021 Prover run. The complete original dependency criterion is unchanged. Primary blockers: old external library package not vendored, scripts rewrite Solidity for harnesses, source/ABI drift, unproven call-resolution and observed Prover version. No modern same-named handler/library should stand in for 2021 code.

## Navigation

- [properties.csv](properties.csv): exactly one row per original unique example, without Bug Label duplication.
- [properties/](properties/): per-example source/status/evidence dossier, target-specific decision and provisional candidate.
- [patterns/](patterns/): reusable official migration guidance and non-mechanical proof obligations.
- [evidence_register.csv](evidence_register.csv): A1/A2/B1 and catalog/transcript provenance with scope of each source.
- [recovery_manifest.csv](recovery_manifest.csv): exact 2021 Git SHA pairs, recoverable paths, blocked imports/version uncertainties.
- [QA_REPORT.md](QA_REPORT.md): count/coverage, evidence closure and no-execution statement.

## Safety/phase boundary

**SEM ALTERAÇÕES EM SPECS; SEM COMPILAÇÃO CVL2; SEM PROVER; SEM TESTE CVL1.** Only documentation is authored here. Future migrations must be derived and separately authorized, without touching source snapshots, `results/spec/`, `contracts/`, `reports/`, or original PDF. Proposed buckets are provisional research labels only.