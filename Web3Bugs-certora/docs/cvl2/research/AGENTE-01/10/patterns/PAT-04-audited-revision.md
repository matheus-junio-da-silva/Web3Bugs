# PAT-04 — Historical revision and dependency reconstruction

Evidence: EV-SRC-CAT, EV-SRC-CLOSURE, EV-UP-COMMIT, EV-UP-PKG, EV-UP-SCRIPT, EV-UP-DRIFT.

The report's audited commit is `c90dec1046e5e26edf70f985dd86381403912482` in `dinngo/furucombo-contract`, now archived. It pins `solc=0.6.12` and `@openzeppelin/contracts=3.3.0`. The catalog snapshot is later; notably *all 22 distinct Original Contract source paths* mentioned by P10 rows have different blobs in the audited commit. `proxy.spec` and `registry.spec` also changed, while the other six used source spec blobs match. Two additional proxy rule names do not exist in the audited commit. Never combine a 2021 compiler/source choice with later 0.8.x code by basename.

Mark each retrieved upstream blob as `RECOVERABLE_WITH_PROVENANCE`, without modifying original `incomplete` status. A recoverable source blob is **not** a complete dependency closure: package lock, external imports, script-generated code, accurate target ABI, and verification config remain open. Do not run Perl mutating scripts on the historical snapshot.

**Not run:** Solidity compilation, npm/truffle, Certora CLI, CVL2 compilation, Prover.