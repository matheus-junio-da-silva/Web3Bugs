# AGENTE-05 — Project 21 / Lido V2 — PHASE 1 RESEARCH (2026-10-19)

- Web3Bugs source HEAD 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3; PropertyGPT source HEAD 687f654c679ed45ab127b7949e2a29c8f5e491b9.
- Source under contracts/21/ and PropertyGPT/certora_projects/lido_v2/; preserved PDF: resources/21/Certora-Lido-V2-Audit-Report-04-23.pdf.
- 2 unique (project,status,example) keys; historical complete 0, incomplete 2.
- Full-file ingestion and individual original-declaration extraction 2/2, including full N.spec/N.md/N.sol and N.txt for each incomplete. Individual PDFs examined by screenshot: 2 distinct pages; all archived PDF SHA256 verified.
- Provisional classifications: {'UNRESOLVED_CANDIDATE': 2}. CANDIDATE means no new compilation or formal proof; all 2 retain uncertainty about semantic preservation under CVL2.

## Document map
- properties.csv: original identity/outcomes, hashes, syntax candidates and research-status fields.
- properties/{complete,incomplete}/N.md: verbatim property body with source coordinates, original assumptions, related methods, historical dependencies, source-level candidate changes and risk.
- evidence_register.csv: official CVL2 rules and per-example file hashes/URLs.
- recovery_manifest.csv: only historically missing dependencies and provenance status.
- patterns/observed-actual-lines.md: actual syntax occurrences indexed by property and line.
- QA_REPORT.md and VALIDATION_LOG.md: source-read coverage, limits and observed validation exit codes.
- PDF_DIRECT_REVIEW.md is available where official PDF pages were visually checked.

## Integrity and unresolved risks
The two DSM rules do not match the 18 named PDF properties. Harness/getGuardianLength absent and authorized quorum may exceed guardian count.
Every property file was read programmatically and inspected for literal rule bodies, requirements and calls; this is NOT a claim of independently reconstructing every historical execution configuration or proving semantic equivalence. Missing authenticated ABI, remappings, compiler/certora versions and audit commit correspondence remain blocking where indicated.

SEM ALTERAÇÕES EM SPECS; SEM COMPILAÇÃO CVL2; SEM PROVER; SEM TESTE CVL1. PR remains DRAFT and no Fase 2 authorization is claimed.
