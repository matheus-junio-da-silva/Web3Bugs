# AGENTE-05 — Project 19 / Origin OUSD — PHASE 1 RESEARCH (2026-10-19)

- Web3Bugs source HEAD 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3; PropertyGPT source HEAD 687f654c679ed45ab127b7949e2a29c8f5e491b9.
- Source under contracts/19/ and PropertyGPT/certora_projects/ousd/; preserved PDF: resources/19/OriginFeb2021.pdf.
- 37 unique (project,status,example) keys; historical complete 2, incomplete 35.
- Full-file ingestion and individual original-declaration extraction 37/37, including full N.spec/N.md/N.sol and N.txt for each incomplete. Individual PDFs examined by screenshot: 0 distinct pages; all archived PDF SHA256 verified.
- Provisional classifications: {'UNCHANGED_CANDIDATE': 2, 'UNRESOLVED_CANDIDATE': 35}. CANDIDATE means no new compilation or formal proof; all 37 retain uncertainty about semantic preservation under CVL2.

## Document map
- properties.csv: original identity/outcomes, hashes, syntax candidates and research-status fields.
- properties/{complete,incomplete}/N.md: verbatim property body with source coordinates, original assumptions, related methods, historical dependencies, source-level candidate changes and risk.
- evidence_register.csv: official CVL2 rules and per-example file hashes/URLs.
- recovery_manifest.csv: only historically missing dependencies and provenance status.
- patterns/observed-actual-lines.md: actual syntax occurrences indexed by property and line.
- QA_REPORT.md and VALIDATION_LOG.md: source-read coverage, limits and observed validation exit codes.
- PDF_DIRECT_REVIEW.md is available where official PDF pages were visually checked.

## Integrity and unresolved risks
Original lockfile pins @openzeppelin/contracts 2.5.0 and upgrades 2.8.0, not recovered. Scripts modify OUSD harness and not all targets are interchangeable.
Every property file was read programmatically and inspected for literal rule bodies, requirements and calls; this is NOT a claim of independently reconstructing every historical execution configuration or proving semantic equivalence. Missing authenticated ABI, remappings, compiler/certora versions and audit commit correspondence remain blocking where indicated.

SEM ALTERAÇÕES EM SPECS; SEM COMPILAÇÃO CVL2; SEM PROVER; SEM TESTE CVL1. PR remains DRAFT and no Fase 2 authorization is claimed.
