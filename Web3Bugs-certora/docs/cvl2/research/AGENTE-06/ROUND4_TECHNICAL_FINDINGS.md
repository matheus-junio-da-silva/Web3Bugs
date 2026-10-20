# AGENTE-06 — Round 4: targeted historical research and CVL2 gates

Date: 2026-10-20. Baseline: \`2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3\`. Research starting HEAD: \`684bd419ee8e35f27ca7ee07138fced321160793\`.

**Scope and methodology:** 159 canonical (project, original status, example ID) keys, P1=70, P4=27, P17=41, P22=21. The accompanying \`ROUND4_PROGRESS_159.csv\` has one distinct row per key and records original paths, SHA-256-confirmed N.spec and ancillary N.md/N.sol/N.txt, archived closure state, observed legacy lexemes, historical runner, actual compilation status, semantic gate and next action. A lexical match in the extracted N.spec includes its copied dependencies and is **not** a proof that the isolated rule executes that syntax. Historical status and report findings are unchanged.

## P1: queue2 / _mock / complexity are distinct obstacles

- In the **archived** \`contracts/1/contracts/bridges/L2BridgeExecutor.sol\`, the callable function is \`queue(...)\`, while \`contracts/1/specs/Optimism_ArbitrumBridge.spec\` repeatedly calls \`queue2(e, args)\`. There is no \`queue2\` implementation or declaration in the archived bridge Solidity. The documented \`queue\` interface and the CVL \`queue2\` symbol must **not** be equated by guessing a wrapper, replacing a method signature or modifying arguments.
- \`_mock(e)\` appears in both Polygon and L2 specs, including \`getGuardian() != _mock(e)\`; its precise historical meaning and binding are not proven by the archived Solidity ABI. It could affect caller-related assumptions. Do not drop or replace this condition.
- \`contracts/1/specs/complexity.spec\` contains parametric \`sanity\`, \`noRevert\`, \`alwaysRevert\`, \`simpleFrontRunning\` and \`privilegedOperation\` rules; \`f@withrevert\`, \`lastReverted\`, snapshots (\`lastStorage\`), method filtering, and \`f.selector\` depend on an authenticated selected contract, methods universe and execution configuration. This does not follow from standalone N.spec extraction.
- The report-referenced source commit \`303bd3e16c8d3465325389a72564126c3bacc4f9\` identifies upstream **Solidity provenance**, not the CVL execution configuration. The source snapshot differs from some audited blobs at \`pragma solidity 0.8.10\` vs \`^0.8.10\`, and \`BridgeExecutorBase.sol\` also differs in a comment. Even seemingly nonsemantic diff does not prove equal compiler selection or full transitive closure.
- Partition retained from previous evidence: **14 queue2**, **6 _mock**, **6 complexity runner**, **44 run unattributed**. Original complete/incomplete is a catalog status, not a source-compilation certificate. Polygon guardian controls and Optimism/Arbitrum cross-domain caller authorization require target-specific validation.

**Potential follow-up examples (not authorized for migration):** P1 complete/1–3 from \`PolygonBridge.spec\` lack a proven historical per-rule job/ABI, but are useful first targets *if* an authenticated Polygon runner and exact audited ABI are recovered. The queue2 family cannot be a diagnostic candidate until its original wrapper is identified.

## P4: generated Solidity is not the root snapshot

- \`contracts/4/certora/Makefile\` has \`CONTRACTS_DIR = ../src\`, \`MUNGED_DIR = munged\`; target \`munged\` runs \`cp -r ../src munged\` then \`patch -p0 -d munged < applyHarness.patch\`. The snapshot contains \`certora/munged/.gitignore\` only, and no archived \`../src\` in \`contracts/4\`.
- \`applyHarness.patch\` changes the actual compiler input (\`override\` at \`StakedTokenV2.getTotalRewardsBalance\`, \`StakedTokenV3.previewStake\`, \`setCooldownSeconds\` and \`getCooldownSeconds\`), not just cosmetic formatting. Importing \`StakedAaveV3Harness.sol\` against root \`contracts/4/contracts/*.sol\` is **not equivalent** to reconstructing \`certora/munged\`.
- The archived runners differ in which spec is selected: \`runAllProps.sh\` selects \`allProps.spec\`, \`runInvariants.sh\` selects \`invariants.spec\`, while \`runPropertiesWithSummarization.sh\` selects \`summarizationsCollector.spec\`. They configure harness files, \`solc8.17\`, token/vault links, \`--optimistic_loop\` and \`--loop_iter 3\`; there is no authenticated original job choosing the exact rule set.
- The PDF pins audited **upstream source** \`4cf8837121a4351cc0e21703bb1df76036205114\`. Existing \`4/AUDITED_SOURCE_PROVENANCE.md\` documents differences between several archived root Solidity blobs and audited \`src\` blobs. Neither the upstream \`src\` tree nor a locally re-applied patch *by itself* authenticates the generated Solidity or the exact Certora build. **27/27 remain incomplete and blocked.**

**Reopening evidence:** historical generated tree/hash plus the matching upstream \`src\` and patch, compiler/runtime versions, selected runner and ABI/links. Do not synthesize the tree as a replacement for authenticated audit evidence.

## P17: Specify 2019 must be adjudicated *per rule and construct*

The **extracted** 41 N.spec files were scanned after removing comments (not by mutating the originals): \`static_assert\` occurs in 41, \`static_require\` in 40, \`sinvoke\` in 41, \`invoke\` in 28, \`havoc\` in 41, and \`lastReverted\` in 11. These are textual counts over *complete extracted spec files*, not counts of verified semantic behaviors. \`ROUND4_PROGRESS_159.csv\` preserves each property's own flags and distinguishes \`havoc\` targets declared as \`env\` from local/undeclared targets.

- **Pre/post state snapshots:** \`complete/8 borrowFresh\` creates \`env e0/e1/e2\`, then \`havoc\`s them; uses \`sinvoke\` for getter observations and \`static_require result == invoke borrowFreshPub(e1,...)\` followed by \`lastReverted\`. Simply applying the CVL2 migration script could change the relation between selected environments, revert outcomes, and assertions. \`complete/9 repayBorrowFresh\`, \`complete/10–15\` related flow rules need the same per-rule check; do not infer identical behavior from similar syntax.
- **Local havoc and domain:** \`complete/8\` and \`complete/9\` also \`havoc other\`; \`complete/39 transferFrom\` includes both \`havoc other\` and \`havoc doApprove\`. The CVL2 guide expressly disallows havocing local variables (as distinct from ghost variables); replacing them with new symbolic values is a *candidate needing domain and correlation analysis*, not an approved translation.
- **Access/admin, frame and wrapper families:** complete/18–21 and corresponding incomplete admin examples contain pre/post state assumptions; complete/22–38 are frame rules with \`sinvoke\` and \`invoke\`; incomplete/7 \`accrueInterest\` additionally lacks an authenticated \`interestRateModelGetBorrowRate()\` ABI binding. Preserve each assertion and method receiver. \`.spclnk\` JSON names model contracts and method bindings (for example \`ComptrollerModel\`); matching Solidity blob hashes alone do not establish original Specify runtime method resolution.
- **Documented CVL1→CVL2 lexer suggestions are NOT Specify-runtime evidence:** official instructions describe \`sinvoke f(...)\`→\`f(...)\`, \`invoke f(...)\`→\`f@withrevert(...)\`, \`static_assert\`→\`assert\` and \`static_require\`→\`require\`, but expressly warn about manual methods/type/call review and vacuity. The guide does not identify the 2019 Specify engine/version or prove its semantics for this historical report.

**Reopening evidence:** executable versioned 2019 Specify language/engine docs plus original \`.spclnk\` setup, exact wrappers/ABI and rule jobs. Do not run transformed rules as proof of old-result preservation.

## P22: archival identical blobs do not date the audit

- Six identities already recorded in \`22/AUDITED_SOURCE_PROVENANCE.md\` include four specs, the runner and \`PopsicleV3Optimizer.sol\`; they match branch \`certora\` commit \`3cb9cb7279a3fb1790b55251a029bb3065606dc8\` dated **2021-11-04**, which is **after** the report's verification period **2021-09-22 to 2021-10-25**. This is provenance of the later snapshot, not a demonstrated audited SHA, and does not identify what earlier commit/run was verified.
- \`spec/scripts/verifyPopsicleV3Optimizer.sh\` selects **only** \`PopsicleV3Optimizer:spec/PopsicleV3Optimizer.spec\` with \`--rule $1\` and links to \`DummyERC20A/B\`, \`SymbolicUniswapV3Pool\`, \`solc7.6\`, \`--loop_iter 1\`. A literal script invocation with a variable parameter is not an execution log that establishes which particular rule ran. The 13 optimizer-source examples remain **historical_run_unattributed**.
- \`FullMathWrapper.spec\` complete/1–3, \`PoolActions.spec\` complete/6 and \`sanity.spec\` complete/20–21 have no authenticated runner in the preserved script. For incomplete/4, \`totalSupply()\` is absent from the required wrapper public ABI; for incomplete/5, \`to\` is an unbound CVL identifier. They are separate problems; neither may be repaired by inventing a getter or variable.

**Potential follow-up:** the 13 optimizer-source rules (P22 complete/7–19) become the next evidence-first group *only after* a pre-audit source revision and per-rule jobs/targets are authenticated. Algebraic FullMathWrapper rules may appear simpler but the single archived runner does not invoke their spec.

## Explicit execution decision

No project has an unambiguous *historical* target + ABI + transitive source closure and exact run selection. Consequently **no isolated CVL2 compilation was justified or run in this round**. No CVL1, Prover, assertions, assumptions, casts, Solidity, configuration or original specs were changed. \`UNRESOLVED_CANDIDATE\` remains the migration state for all 159. The gate is lack of evidence, **not** a failed CVL2 compilation or a finding.

## Sources (versioned/archive)

- Catalog requirements: \`docs/spec_catalog.md\`, \`docs/spec_catalog_workflow.md\`, \`docs/spec_catalog_project_1.md\`; taxonomy: \`docs/standard.md\`.
- Archived project sources/notes: \`contracts/{1,4,17,22}\`, \`reports/{1,4,17,22}.md\`, \`results/spec/{complete,incomplete}/{1,4,17,22}\`, and \`docs/cvl2/research/AGENTE-06/{1,4,17,22}/AUDITED_SOURCE_PROVENANCE.md\`.
- [Certora CVL2 migration](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html), [Certora CVL2 changes](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html).
- [P1 report-linked upstream source commit](https://github.com/Certora/governance-crosschain-bridges/commit/303bd3e16c8d3465325389a72564126c3bacc4f9), [P4 report-linked source commit](https://github.com/Certora/aave-stk-v1-5/commit/4cf8837121a4351cc0e21703bb1df76036205114), [P17 report-linked source commit](https://github.com/compound-finance/compound-protocol/commit/f385d71983ae5c5799faae9b2dfea43e5cf75262), [P22 later Certora branch](https://github.com/Popsicle-Finance/PopsicleV3Optimizer/commit/3cb9cb7279a3fb1790b55251a029bb3065606dc8).

**AGENTE-06 — RODADA 4.**
