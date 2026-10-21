# AGENTE-06 — independent read-only review, AGENTE-07 PR #41

Review date: 2026-10-20. PR https://github.com/matheus-junio-da-silva/Web3Bugs/pull/41.

- Immutable reviewed HEAD: \`78800bb132f9a40d7db4d5ae3e3bbb99c2c884c8\`.
- Original baseline: \`2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3\`.
- Review performed by reading local Git objects at those **explicit SHAs** in an independent, pre-existing agent-07 clone \`/home/mat/cvl2-agent07-isolated/Web3Bugs\`. Its checked-out HEAD was older; **no checkout, commit, push, branch update, file edit or review comment** was made to AGENTE-07/PR #41. GitHub PR HEAD was independently checked first.

## Mechanical gate — previously outstanding, now executed

The following exact semantic equivalent of the requested \`BASE...HEAD\` Git command was executed, with the **current reviewed SHA** substituted for \`HEAD\` because the working directory is intentionally on an older checkout:

\`\`\`bash
git -c core.whitespace=cr-at-eol diff --check \
  2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...78800bb132f9a40d7db4d5ae3e3bbb99c2c884c8
# observed EXIT 0
\`\`\`

Independent \`git diff --name-only BASE...REVIEWED_SHA\` counted **217 changed files**, zero outside \`Web3Bugs-certora/docs/cvl2/research/AGENTE-07/\`. Unlike the previous patch-only GitHub API checks, the Git check was actually executed against the complete committed diff of the reviewed SHA.

## Independent sample and per-instance corroboration

The four \`full_spec_audit.csv\` documents were loaded **from the reviewed commit**, and their 156 rows were individually checked against the corresponding archived \`results/spec/.../N.spec\` bytes in the same Git tree. Checks: canonical-key uniqueness, SHA-256, byte lengths, and incomplete \`N.txt\` SHA-256 where the matrix provides one. Results: **156/156 pass**: P8 42; P9 61; P11 16; P20 37. This confirms source fingerprint/traceability, not CVL2 syntax or semantic validity.

Source-closure findings corroborated with \`UPSTREAM_CHECKS.md\` and \`QA_REPORT.md\` at the same commit:

| Project | Supported evidence | Still not proven |
|---|---|---|
| **P8 AAVE Vault** | 22 extracted instances flagged W1 (rayMul global axiom), 1 flagged W2/W3 (zero-denominator global axioms), 19 do not exhibit *these* contradictions; archived axioms preserved | Satisfiability/non-vacuity, execution equivalence; \`VERIFIED\` is only the reported original result |
| **P9 Celo** | 61 stable keys; two archived Celo Governance.sol phase blobs differ from one another and from the snapshot; three \`governance_old_rules.spec\` examples retained | Selection of audited phase/ABI/compiler for each rule; 50 DOCUMENTED_CANDIDATE are lexical, not approved |
| **P20 BentoBox** | Exact BoringSolidity lockfile commit \`39fdd3b4...\`, source blob comparison; runner patching of harness/\`node_modules\` identified | Transformed source build, \`MAX_INT()\` call lacking definition in \`compoundStrategyAdditional.spec\`, verified call/exception summaries |
| **P11 Keep** | Three npm tarball SRI checks and 22/22 direct external import paths documented | Transitive import/semver resolution (nested openzeppelin 2.4.0 vs top-level 2.3.0), original audit commit/runtime |

## Independent disposition

**Documentary and whitespace gate: PASS for HEAD 78800bb. Migration gate: UNRESOLVED.**

No basis found to upgrade any source-closure claim to proved, grant CVL2 phase 2 authorization, adjust axioms/assertions/assumptions, or merge. This review is documentary and static only: **no CVL1, CVL2 compilation, Certora Prover or historical replay**. Keep PR #41 Draft. Reopen cases only on authenticated source/runner/ABI evidence.

**AGENTE-06 — RODADA 4 (independent read-only peer review).**
