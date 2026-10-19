# QA — AGENTE-05 / P21

- Source HEAD 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3; PropertyGPT HEAD 687f654c679ed45ab127b7949e2a29c8f5e491b9. Branch research/cvl2-agente-05 isolada.
- Directory listing `results/spec/incomplete/21/` verified: two numbered `.spec`, 2 `.md`, 2 `.txt` and 2 `.sol`. `complete/21/` absent, consistent with zero complete. Keys: (21,incomplete,1), (21,incomplete,2), no duplication.
- Two dedicated dossiers; two CSV rows; both properties have explicit incomplete reasons; labels preserved as UNMAPPED. Names differ from PDF tests; no propagation of 18 published DSM verifications.
- Evidence IDs A1 and H21 checked against source paths and official CVL2 documentation, but an official revision-pinned document and true audited harness commit were not recovered.
- Main finding: non-revert rule tests positive success unconditionally; quorum invariant conflicts with intentionally permitted quorum setting in production code; **both need original harness before executable semantics may be established**.
- Validation: documentary count by GitHub directory listing and metadata cross-check. **No repository validator, git diff --check, CVL compilation, Certora Prover or CVL1 test executed here**; GitHub remote connector has no running checkout and Desktop Commander device was offline.
- Follow-up reviewer: require original harness plus source/commit, confirm ABI, then adjudicate whether any syntactic edits preserve all revert paths/quantifier spaces. Do not promote candidate status without experiments.
