# AGENTE-01 — QA Report (FASE 1)

- Input Web3Bugs/main: `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`; PropertyGPT/main: `687f654c679ed45ab127b7949e2a29c8f5e491b9` (both checked 2026-10-19).
- Reconciliation in `results/spec/spec_buglabel.csv`: 266 Project ID 10 rows, 266 unique keys, 2 complete / 264 incomplete; status/Example ID uniqueness checked in-memory with a CSV-quote-aware parser. 31 unique property names represent 34 CVL declarations and target expansions.
- Source repository verified at archived upstream `dinngo/furucombo-contract` SHA `c90dec1046e5e26edf70f985dd86381403912482`. Git tree comparisons: 22/22 distinct P10 target Solidity original-source paths have **different** Git blob SHAs from snapshot (do not treat as identical); `proxy.spec` and `registry.spec` differ; other six original source spec paths have identical blobs.
- The original 2021 report is the authority for audit scope; text `reports/10.md` was consulted, but the PDF's physical table layout was **not independently visually revalidated** in this run. This is a remaining limit.
- **Critical risks:** missing exact compiler + Prover run reconstruction; pinned but unvendored OpenZeppelin 3.3.0; per-handler Perl-transformed ABI and injected getter source; summary receiver/sighash changes; later rules absent at original audit SHA; multi-target proof inflation.
- **Allowed validation:** GitHub tree/read-only file SHA check, source-line inspection, key reconciliation, official documentation review. No checked-in source change. Final Git diff and dossier counts to be reconciled after creation.
- **Not run:** no Certora CLI, no Solidity compiler, no scripts modifying source, no CVL1 tests, no CVL2 compiler, no Prover. No claim of semantic equivalence, execution, VERIFIED or VIOLATED as a new result.
- **Review decision:** keep PR draft; future Fase 2 requires explicit coordinator permission.
## Final documentary reconciliation — 2026-10-19

- Recount: exactly 266 per-example dossiers (264 incomplete, 2 complete), and 266 unique rows in properties.csv. 264 incomplete N.spec and 264 N.txt blob entries confirmed. GitHub compare showed exactly 277 added files, all inside the sole authorized research directory. Zero edits to historical artifacts.
- Evidence: 20 registered entries; 32 recovery-manifest records; no orphan evidence IDs in the 266-row table. Every bucket provisional and ends with _CANDIDATE.
- Audit SHA c90dec1046e5e26edf70f985dd86381403912482 retrieved from archived dinngo/furucombo-contract; package.json pins solc 0.6.12, OpenZeppelin 3.3.0, Truffle 5.1.60. All 22 distinct listed original target Solidity files have different audited versus saved blob SHAs. Two of eight source CVL files differ (proxy.spec and registry.spec).
- Rule names nonExecutableWhenProxyIsBanned and nonExecutableWithInitializedSender are absent at the audited 2021 proxy.spec. Other old/current proxy rule bodies differ; 2021 outcomes are not transferable without proof.
- Limitation: original eight CVL source texts and per-entry CSV metadata were reviewed, but 264 N.txt and 266 N.md were NOT each reread end-to-end in this new pass. Each dossier is a provisional source/target research entry, not certified dependency closure. This remains an explicit independent-review blocker.
- Limitation: Certora report transcript reviewed; physical PDF table layout not visually verified. No current build/Prover version identified.
- Execution: local execution environment reported ClientError, Desktop Commander device offline. Thus neither git diff --check nor Python catalog validators were executed; only GitHub contents/tree/compare API checks succeeded (no shell exit codes).
- Phase boundary: SEM ALTERAÇÕES EM SPECS; SEM COMPILAÇÃO CVL2; SEM PROVER; SEM TESTE CVL1. Never promote candidate to compiled bucket or merge until independent review.
