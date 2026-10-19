# PAT-06 — Original run and compiler reconstruction

Evidence: EV-A1-CLI, EV-UP-PKG, EV-UP-SCRIPT and EV-SRC-HANDLER. Historical scripts use `--verify`, `--settings`, loop/unroll `-b=2`, `-b=3` or `-b=64` and `-assumeUnwindCond`; a `--settings` → modern CLI mapping must be checked against actual CLI/version before execution. CLI syntax changes from v4.3.1 in official Certora docs.

In Fase 1 do not execute these scripts because they rewrite Solidity, create harnesses or invoke a Prover. Record target, script, exact parent commit, compiler and external package missing pieces. `N.sol` is documentary evidence, not a standalone compile unit. **No runs performed.**