# AGENTE-05 — honest QA coverage status: Project 6

## Structural reconciliation (finished)
- At confirmed Web3Bugs SHA `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`, inventory contains 32 unique numeric .spec examples; properties.csv has exactly 32 records after proper canonical-key deduplication. Original Bug Labels, Result and Detection Outcome preserved from catalog CSV. README and evidence register contain version-pinned source pointers.
- The same number of `properties/<status>/<N>.md` files exists in this research branch. **This does not mean their source-level semantic research is complete.**

## Depth of research at current commit
- Direct reading of extracted .spec and N.txt: **8/32** cases; remaining **24** dossiers transparently describe metadata-level triage and explicitly mark missing line-specific migration evidence. For complete examples the N.txt does not exist.
- Target/harness and original ABI lack authenticated linkages; source reviewed for first eight only.
- Every record is **UNRESOLVED_CANDIDATE** and bucket 02_unresolved candidate, because no compiler/error log or semantic equivalence test has been run. No summary implies compile success. Specific source-reading progress must be revised as further direct reads are committed.

## Important limitations
- The historical files remain unmodified. The per-example source links and Git blob hashes show provenance but are not proof that all bodies were reviewed.
- Not run: CVL2 compiler, Certora Prover, CVL1 tests, source restoration, python validation scripts, git diff --check on a current checkout. Remote Desktop Commander device is offline and attached ZIP has stale main SHA. No invented exit codes.
- Do not request Phase 2 or merge until each remaining N.spec and missing N.txt and N.md has a true per-case semantic analysis, plus independent QA and explicit coordinator approval.
