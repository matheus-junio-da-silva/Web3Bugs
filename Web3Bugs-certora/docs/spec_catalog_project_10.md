# Project 10 — Furucombo: source-preserving Certora property catalog and closure audit

> **Review status: DRAFT / NOT VALIDATED.** This ledger contains 36 target-aware examples for 34 active declarations. It is not a reproduced 2021 verification result or a completed handler-by-handler execution matrix. Do not merge until the below blockers and validation have been reviewed.

## 1. Identity, preservation and provenance

- **Original repository:** `matheus-junio-da-silva/PropertyGPT`, `certora_projects/furucombo/`.
- **Destination:** `matheus-junio-da-silva/Web3Bugs`, `Web3Bugs-certora/`, branch `catalog/p10-gaia-furucombo`.
- **Source snapshot:** precisely **202 files** from the source's `contracts/` and `specs/` tree were copied byte-for-byte to `contracts/10/`; a renewed comparison of Git blob SHA found **202/202 matches** against the PropertyGPT tree. The source project has 203 blobs counting the separately preserved PDF. Unchanged source code is never repaired in place.
- **Historical PDF:** `resources/10/FurucomboMay2021.pdf` is identical to PropertyGPT `FurucomboMay2021.pdf` and Certora/SecurityReports `Reports/2021/04_21_2021_Furucombo-FV.pdf`, blob `fa3483cd8b7c7bce2e472b217c2531a0f0965515`. Text extraction: `reports/10.md`, **31 pages**; the PDF controls for table layout and symbols.
- **Historical verified code:** report says last reviewed revision `c90dec1046e5e26edf70f985dd86381403912482`, audited 15 March–12 April 2021. The copied Solidity sources are from another era (Solidity 0.8.10); identical semantics or proof results cannot be assumed.

## 2. Inventory and example accounting

| CVL file | Active declarations | Included examples |
| --- | ---: | --- |
| `specs/proxy.spec` | 17 (16 rules, 1 invariant) | 13–29 for the generic ProxyHarness context; handler-target variants remain to be reconciled |
| `specs/registry.spec` | 10 rules | 1–10 |
| `specs/privileged.spec` | 1 rule | 11 (Registry) and 12 (Proxy), distinct scripts and targets |
| `specs/hbalancer.spec` | 1 rule | 30, HBalancer **incomplete** |
| `specs/hmaker.spec` | 1 rule | 31 (HMaker) **and 36 (HBProtocol)**, with different contract constants and unroll limits |
| `specs/hscompound.spec` | 1 rule | 32 (HSCompound) |
| `specs/libParam.spec` | 2 rules | 33 and 34 |
| `specs/sanity.spec` | 1 diagnostic rule | 35 |
| **Total** | **34 active declarations** | **36 source/target instantiations** |

Commented blocks `proxy.spec:558–578` containing `holdNoEth` and `onlyValidCaller` are **excluded** as inactive; the latter is nonetheless cited in a 2021 report finding. Do not turn that reference into a current active example. **29 dependency-complete and 7 incomplete examples** are indexed; neither class guarantees historical Prover reproducibility. Complete is a narrow non-built-in symbol-resolution status, not a proof run.

The 36-example inventory is **not** a full Cartesian product of `proxy.spec` × handler scripts: the original handler-facing driver invokes `proxy.spec` with different target contracts. Each generic per-target invocation still needs per-handler assertion/result interpretation. No `VERIFIED` or `VIOLATED` is borrowed from one handler for another.

### Explicit incomplete examples

| ID | Property | Missing dependency / reason |
| --- | --- | --- |
| 15 | `startStateCleanup` | `ProxyHarness.getStackLengthSlot` uses missing Solidity `stack_slot` |
| 16 | `noOverwrite` | same `stack_slot`; memory-stack High report issue is a distinct kind of memory safety |
| 19 | `cubeCounterIsAlwaysCleanedUp` | `ProxyHarness.getCubeCounter` calls absent inherited `_getCubeCounter()` |
| 20 | `cacheIsAlwaysCleanedUp` | `CUBE_COUNTER_KEY()` CVL getter lacks matching original Solidity implementation |
| 23 | `nonExecutableWithUninitializedSender` | CVL three-argument `proxy.batchExec` selector vs four-argument current Solidity ABI |
| 29 | `cubeCounterGreaterThan0IffSenderInitialized` | inherited `_getCubeCounter()` absent |
| 30 | `executeDelegatesOnlyToAllowedAddresses` (HBalancer) | handler `contracts/handlers/balancer/HBalancer.sol` absent in exact historical path |

The relevant `N.txt` files identify missing dependencies; no substitute is fabricated. Separate `ProxyHarness.sol`/current-`Proxy.sol` compile mismatches described below affect **all** ProxyHarness examples even if they are categorized complete by the narrow catalog rule.

## 3. Historical handler matrix — all 23 named in report

The report's handler list is **historical**. Paths are under `contracts/10/contracts/handlers/`; scripts are under `contracts/10/specs/scripts/`. PRESENT means a blob with the same name exists in the copied snapshot, **not** that it is the same deployed/audited version.

| Handler in 2021 report | Source in snapshot | Available driver | Closure / result caution |
| --- | --- | --- | --- |
| `HMaker` | `maker/HMaker.sol` | runHMaker.sh; runHMakerSpecific.sh | 31 — HMaker-specific rule, plus generic proxy.spec target pending |
| `HAaveProtocol` | `aave/HAaveProtocol.sol (MISSING)` | runHAave.sh | missing source; generic run cannot compile as preserved |
| `HAaveProtocolV2` | `aavev2/HAaveProtocolV2.sol` | runHAave2.sh | generic proxy.spec handler result not independently attributed |
| `HSCompound` | `compound/HSCompound.sol` | runHSCompound.sh; runHSCompoundSpecific.sh | 32 — specific rule, generic rule result pending |
| `HFunds` | `funds/HFunds.sol` | runHFunds.sh | generic handler result pending; p.4–5 concrete findings |
| `HOneInchExchange` | `oneinch/HOneInchExchange.sol (MISSING)` | No corresponding script | different HOneInchV5 is not historical substitute |
| `HBalancer` | `balancer/HBalancer.sol (MISSING)` | runHBalancer.sh; runHBalancerSpecific.sh | 30 — incomplete; cannot substitute another Balancer implementation |
| `HCEther` | `compound/HCEther.sol` | runHCEther.sh | generic proxy.spec result pending |
| `HCToken` | `compound/HCToken.sol` | runHCToken.sh | generic proxy.spec result pending |
| `HGasTokens` | `gastokens/HGasTokens.sol (MISSING)` | runHGasTokens.sh | script references absent target |
| `HStakingRewardsAdapter` | `staking/HStakingRewardsAdapter.sol` | runHStakingRewardsAdapter.sh | generic proxy.spec result pending |
| `HUniswapV2` | `uniswapv2/HUniswapV2.sol` | runHUniswapV2.sh | generic proxy.spec result pending |
| `HCurve` | `curve/HCurve.sol` | runHCurve.sh | generic proxy.spec result pending |
| `HCurveDao` | `curve/HCurveDao.sol` | runHCurveDao.sh | generic proxy.spec result pending |
| `HWeth` | `weth/HWeth.sol (MISSING)` | No corresponding script | HWrappedNativeToken is not same historical handler |
| `HYVault` | `yearn/HYVault.sol` | runHYVault.sh | generic proxy.spec result pending |
| `HKyberNetwork` | `kybernetwork/HKyberNetwork.sol (MISSING)` | No corresponding script | cannot infer via other swap handlers |
| `HSushiSwap` | `sushiswap/HSushiSwap.sol` | runHSushiSwap.sh | generic proxy.spec result pending |
| `HUniswap` | `uniswap/HUniswap.sol (MISSING)` | No corresponding script | HUniswapV2/V3 are not HUniswap |
| `HMooniswap` | `mooniswap/HMooniswap.sol (MISSING)` | No corresponding script | no historical source in snapshot |
| `HFurucomboStaking` | `furucombo/HFurucomboStaking.sol` | runHFurucomboStaking.sh | generic proxy.spec result pending |
| `HComptroller` | `compound/HComptroller.sol` | runHComptroller.sh | generic proxy.spec result pending |
| `HBProtocol` | `bprotocol/HBProtocol.sol` | runHBProtocol.sh; runHBProtocolSpecific.sh | 36 — hmaker.spec with target-specific actions address and -b=2 |

- **15 named implementations present, 8 absent.** The missing historical names are `HAaveProtocol`, `HOneInchExchange`, `HBalancer`, `HGasTokens`, `HKyberNetwork`, `HMooniswap`, `HUniswap` and `HWeth`. No similarly named modern handler is substituted.
- The original shell driver `_runHandler.sh` (lines 32–38 and 66–115) rewrites handler sources and interfaces before calling Certora. Scripts for HMaker/HSCompound-specific checks use `-b=3` whereas `runHBProtocolSpecific.sh` reuses `hmaker.spec` on `HBProtocol` with **default `-b=2`** and a different `getProxyActions()` override. Their historical outcomes are kept independent.
- Newer script targets present in the snapshot but **not among the 23 historical handlers** include `HOneInchV5`, `HGelatoV2LimitOrder`, `HPolygon`, `HUniswapV3` and `HWrappedNativeToken`. These are not evidence for missing historical targets. Their generic `proxy.spec` run results remain `NOT_STATED` unless independent report evidence exists.
- `🔎` in report tables means per-function detail follows; a table cell `None` is not equivalent to a universal `✔` for the extracted modern rule. The status of handler-specific row outputs must not be propagated to other handlers.

## 4. Semantic second audit and non-proofs

### A. Generated token balance is compared with itself

The source `proxy.spec:509–532` declares `storage initialStorage` and reads `origConsumedTokenBalance` **at** `initialStorage` (line 526), but reads `origGeneratedTokenBalance` without `at initialStorage` at line 527. `updatedGeneratedTokenBalance` at line 524 is also a post-call read. For a stable `Summary.getBalance` and no intervening storage mutation, the second assert (line 530) reduces to a strict self-comparison `x > x` when its antecedent holds. This is a property/specification defect; it must **not** be interpreted as evidence of an actual token conservation violation. The original CVL is preserved exactly; example 27 is `S6-4 / NOT_STATED / NOT_STATED`.

### B. Selector and harness ABI mismatch

- `proxy.spec:456` calls `proxy.batchExec(address[],bytes32[],bytes[]).selector`. The preserved `Proxy.sol:97–102` instead has `batchExec(address[],bytes32[],bytes[],uint256[])`; example 23 is **incomplete**, with no replacement method invented.
- `specs/harnesses/ProxyHarness.sol:6` invokes one-argument `Proxy(registry)`, while `contracts/Proxy.sol:55` requires `Proxy(registry_,feeRuleRegistry_)`. Harness `_exec(address,bytes)` differs from `Proxy._exec(address,bytes,uint256)`; `_parse`, `_trim` and `_execs` also require source version reconciliation. Handler driver source rewrites and `applyHarnesses.sh` reductions from a 256-slot local stack to 2-slot models preclude a naïve modern build.
- `stack_slot`, inherited `_getCubeCounter()` and key-getter ABI dependencies remain unresolved as documented above. Declaring a CVL `methods` entry does not synthesize the missing Solidity symbol.

### C. Authority, bans, cleanup and accounting

- `privilegedOperation` compares two different caller identities and independently quantified calldata from the *same initial storage*. It rejects cases where **both** calls succeed; it does not prove the sole authorized caller is the owner. `knownAsNonPrivileged(method f) = false` does not filter genuinely non-privileged methods. Examples 11 (Registry) and 12 (Proxy) are **NOT_STATED** per target even though a smaller group of historical Registry operations is ✔.
- `nonExecutableWhenProxyIsBanned` directly checks `registry.bannedAgents(currentContract)`, whereas the report's more general banned-caller/agent formulation is not textually equivalent. The related Low issue is recorded in `results/bugs.csv` without treating the exact current-source rule as individually ❌. Example 21: **NOT_STATED / NOT_STATED**.
- `transferredTokensMeanThatStackIsUpdated` has a stronger counterexample mapping to **S3-1 (missing post-process stack update)** than S3-2. `approvedTokensAreTemporary` likewise concerns omitted approval cleanup (S3-1). `noOtherPartyModified` detects unauthorized mutations of unrelated balances (S3-2).
- `notTouchingCache`, `proxy.spec:sanity`, and standalone `sanity.spec:sanity` are diagnostics, not direct vulnerability guarantees; use **UNMAPPED**. The standalone sanity file supplies no trustworthy unique target or report result. `stackLengthIncreaseIsBounded` is an arbitrary bounded-growth sanity bound and maps conservatively to **UNMAPPED**.
- `noOverwrite` checks storage words via `getSlot`, not the local memory overwrite that caused the report's single High issue. Example 16 may be `VERIFIED` for historical storage behavior yet separately connected with a Medium reentrancy-related finding; that does not turn it into a memory-safety detector.
- `getSender()`/`getCubeCounter()` are model/harness-specific; an invariant `counter>0 <=> sender != 0` fails in **both** inconsistent directions, not just when sender is absent.
- Handler `executeDelegatesOnlyToAllowedAddresses` asserts `lenDelegated() <= 3` and that every recorded target matches a handler-specific allowed address. `Summary.checkDelegated()` (`Summary.sol:80–88`) is **vacuously true when `delegated` is empty**; this does not require an actual delegatecall. The model's `Summary.execute` stores addresses and havocs modeled token state; it does not execute a real DSProxy. Four distinct target contexts are cataloged as **L6**: HBalancer (30), HMaker (31), HSCompound (32) and HBProtocol (36).
- `libParam.spec:noThrow` asserts no *throw* (with special non-static `getParams` branch), while `noRevert` forbids most reverts and explicitly excludes `getParams`. These are separate properties, neither individually given a 2021 outcome in the report.

### D. Verification symbols and historical assumptions

The report's **✔** is a verified result on the latest reviewed version; **✔\*** indicates proof under model simplifications/assumptions; **❌** identifies a *test-version* violation; **🔎** refers to function-by-function detail (not uniform VERIFIED). Registry report properties combine `changesHandler + deprecatesHandler` and `changesCaller + deprecatesCaller`: each constituent is **NOT_STATED** for its own formal `Result` unless independently documented. Specific Low finding attribution can coexist as a separate `Detection Outcome = FINDING` when the report directly describes deprecating through registration.

`proxy.sh` uses `-assumeUnwindCond,-b=2`; generic handler scripts default to `-assumeUnwindCond,-b=2,-ciMode=true`; specific HMaker and HSCompound scripts use `-b=3`; `libParam.sh` uses `-b=64,-smt_bitVectorTheory=true`. The report explicitly states unsafe inline assembly was simplified and external DeFi implementations were not formally verified. A 2021 assertion result is **not** a proof about the preserved later Solidity or current Certora toolchain.

## 5. Findings inventory — no invented report issues

The original report enumerates **1 High + 6 Medium + 7 Low issue rows**, plus **2 recommendations**. Exactly **14 rows** `FUR-01` through `FUR-14` were indexed as historical findings in `results/bugs.csv`, with the separate predicates/classes and report references. The report's single Low row *“2 issues: Halting can be irreversible; banning can be irreversible”* is **one grouped severity row** documenting two related irreversible states, not duplicated into two Low CSV rows merely to inflate the report's count.

The 2 explicit **recommendations**, which are not automatic findings, are: (1) simplify the Proxy `_execs` and LibParam loops for readability and (2) use an immutable registry address to prevent a malicious delegatecall from overriding its storage slot. Neither is inserted as an additional finding. The High local memory overwrite is distinct from CVL `noOverwrite`; the report-named `onlyValidCaller` rule is commented out in current source and cannot be called active.

Bug Labels in the bug inventory classify the *documented concrete issue*. Bug Labels in `spec_buglabel.csv` instead classify the *hypothetical assertion counterexample*. These need not agree and are never proof statuses. The names of rules, issue severity, and `O6` cannot independently justify `FINDING` or `ACCEPTED_BEHAVIOR`.

## 6. Artifact manifest and dependencies

- `contracts/10/` — 202 unchanged source files from PropertyGPT.
- `resources/10/FurucomboMay2021.pdf` — original identical PDF.
- `reports/10.md` — page-aligned textual extraction of 31-page original.
- `results/spec/complete/10/` — examples not missing named declarations as assessed.
- `results/spec/incomplete/10/` — examples with `N.spec`, `N.sol`, `N.md`, **`N.txt`** explaining a concrete missing symbol or target.
- `results/spec/spec_buglabel.csv` — **36** new indexed example rows for Project 10; `results/contests.csv` — one Project ID 10 row; `results/bugs.csv` — **14** 2021 finding rows.
- Each `N.spec` reproduces its active property and selected *available* CVL dependencies without rewriting the original assertion. Extra methods in the original full-model `methods{}` block may control symbolic dispatcher behavior; a minimal excerpt is **not** a stand-alone verifier job or a guarantee of model equivalence. The original full spec remains available in `contracts/10/specs/`.

## 7. Unresolved verification and release gates

**Command results: NOT RUN (no evidence of execution).** GitHub Git-object reading/writing was available, but the execution container could not clone GitHub owing to DNS/network failure and the authorized remote desktop was offline. These exact commands must still run on a checkout of this branch from the `Web3Bugs-certora` working directory:

```bash
python scripts/check_specs.py .
python scripts/check_contests_csv.py .
python scripts/check_contracts.py .
git diff --check
```

**Open blockers before final approval:** (1) run actual structural and byte-identity validators; (2) independently reconcile generic `proxy.spec` execution and report `🔎` per handler/selector — do not multiply generic success or failure; (3) decide missing eight historical handlers and same-name but version-shifted contracts without substituting a modern target; (4) resolve or explicitly waive historic harness constructor/`_exec` mismatch and missing symbols before claiming prover reproducibility; (5) independently review issue-label mapping, source-range metadata, and the seven incomplete entries. A **Draft PR**, not a ready-to-merge PR, is appropriate until these gates are satisfied.

**Execution discipline:** source originals were not edited; no private auditor reasoning was invented; no merge or self-approval was attempted. Results and outcomes remain separate in every row.

## 8. Per-target report reconciliation (historical pages 19–31)

This matrix records **each of the 23 historically reported targets** independently. It is evidence of the report's stated *violating functions* and **not** evidence that the exact preserved 0.8.10 source was proved. “None” means no violating functions were listed in the indicated report table, not an independently attributable `VERIFIED`. “N/A” means the report did not consider that property applicable. “Expected” and “overapprox” are report interpretations, not independently recovered current counterexamples. Names are preserved exactly; the eight absent implementations are **not** substituted.

| 2021 handler | Source | #22 stack-on-receipt (p19–20) | #23 temporary approvals (p21–22) | #24 DSProxy allowlist (p23) | #25 token movements (p24) | #26 nonparty balances (p25) |
| --- | --- | --- | --- | --- | --- | --- |
| `HMaker` | present | overapprox: DSProxy operations | None | None | N/A DSProxy | N/A DSProxy |
| `HAaveProtocol` | absent | redeem overapprox; flashLoan expected | None | N/A | None | flashloan potential callback |
| `HAaveProtocolV2` | present | flashloan: nonzero mode | None | N/A | None | flashloan potential callback |
| `HSCompound` | present | overapprox: DSProxy, market methods | None | None | N/A DSProxy | N/A DSProxy |
| `HFunds` | present | None | None | N/A no intermediate | N/A no intermediate | inject/sendToken/sendTokens expected |
| `HOneInchExchange` | absent | None | None | N/A | swap | None |
| `HBProtocol` | present | overapprox: DSProxy operations | None | None | N/A DSProxy | N/A DSProxy |
| `HBalancer` | absent | None | None (join*) | None (join*) | exitswapPoolAmountIn; join* N/A | join* N/A |
| `HCEther` | present | redeem/redeemUnderlying expected ETH | None | N/A | None | None |
| `HCToken` | present | None | None | N/A | None | None |
| `HComptroller` | present | claimComp expected (proxy itself) | None | N/A | None | claimComp expected |
| `HCurve` | present | exchange/removeLiquidity* addressed | exchange*/addLiquidity*; dust expected | N/A | exchange/exchangeUnderlying | None |
| `HCurveDao` | present | None | deposit | N/A | None | mint/mintMany expected |
| `HFurucomboStaking` | present | claimAll expected overapprox | None | N/A | None | None |
| `HGasTokens` | absent | None | None | N/A | None | None |
| `HKyberNetwork` | absent | None | None | N/A | swapTokenToToken | None |
| `HMooniswap` | absent | None | None | N/A | deposit/withdraw: min may be zero | None |
| `HStakingRewardsAdapter` | present | None | None | N/A | None | None |
| `HSushiSwap` | present | None | add/remove liquidity variants | N/A | None | None |
| `HUniswap` | absent | None | None | N/A | tokenToTokenSwap | None |
| `HUniswapV2` | present | None | add/removeLiquidity / ETH caveats | N/A | None | None |
| `HWeth` | absent | None | None | N/A | None | None |
| `HYVault` | present | None | None | N/A | deposit/withdraw may produce zero | None |

**Per-handler six additional table checks:** report properties **#27 bounded stack**, **#28 sender cleanup**, **#29 cube-counter cleanup**, **#30 cache cleanup**, **#31 flat-slot cleanup**, and **#32 flat-slot non-overwrite** each show **“None” for all 23 handlers** (PDF pp26–31). This should be read as a *report-table observation for each individual handler*, not as proof of complete symbol closure or of a later Solidity build. Their closest source rules are `stackLengthIncreaseIsBounded` (17), `senderIsAlwaysCleanedUp` (18), `cubeCounterIsAlwaysCleanedUp` (19), `cacheIsAlwaysCleanedUp` (20), `startStateCleanup` (15) and `noOverwrite` (16). In the copied harness, examples 15, 16, 19 and 20 remain incomplete, independently of the 2021 report-table “None”.

### Executed entrypoint and required target-specific follow-up

`_runHandler.sh:114–118` calls `certoraRun <individual handler>.sol ... --verify ${handler}:${spec} --settings -assumeUnwindCond,-b=${B},-ciMode=true`; `B` defaults to **2**. Thus `runHMaker.sh` (for example) selects **HMaker as target**, not `ProxyHarness`, even though the same `proxy.spec` is used. Fifteen historical names have a same-named file and a generic `run*.sh` driver. **Three drivers** reference absent historical implementations (`HAaveProtocol`, `HBalancer`, `HGasTokens`); **five additional historical targets** lack both a matching source file and a corresponding run script (`HOneInchExchange`, `HKyberNetwork`, `HMooniswap`, `HUniswap`, `HWeth`). A same-named file is not evidence of identity with the 2021 commit.

**Important scope finding:** The existing 36 indexed examples enumerate all **34 active declarations** and four DSProxy allowlist target contexts, but they do **not** enumerate every **material `proxy.spec` × handler** target instance as an individual `N.spec/N.sol/N.md` record. Since the target contract, execution script, method universe and report observations differ, at minimum each of the 15 same-named generic handler targets must receive an individual applicability/dependency assessment against the 11 report-table checks above; the eight missing sources require explicitly unresolved target contexts. Some of those checks have distinct counterexamples (e.g. `HCurve`/approval reset, `HFunds`/third-party balances, `HYVault`/zero output) and cannot be collapsed into `ProxyHarness` or another handler. An *unreconciled* context is not silently counted `complete`. The 36-example figure is therefore a **baseline**, not a certified exhaustive per-target cardinality. This is a **blocking coverage gap** for declaring the catalog final; keep PR #8 draft.

### Scope of these report results vs source formulas

- Report #22 corresponds most closely to `transferredTokensMeanThatStackIsUpdated`, but historical function-level “violating functions” may be expected/overapproximated and do not prove a failure of the later exact assertion.
- Report #23 is broadly approval-cleanup; the modern `approvedTokensAreTemporary` references modeled allowance and may not encode the same single-handler assumption as the report pseudocode.
- Report #24 applies `hmaker.spec` to **HMaker and HBProtocol**, `hscompound.spec` to **HSCompound**, and `hbalancer.spec` to **HBalancer**; distinct target address constants and different `-b` settings prohibit transplanting a result, even though each table cell says “None”. The 4 indexed contexts remain `NOT_STATED` in their formal `Result` fields.
- Report #25 is **not equivalent to conservation** under the preserved `tokenMovementCorrectness` because the generated pre-balance is read without `at initialStorage` (`proxy.spec:527`), causing a potential post-state strict self-comparison.
- Report #26 is not a general “no one else ever changes balance” guarantee: `noOtherPartyModified` excludes modeled addresses and treats callback effects under abstractions; the `HFunds`, `HComptroller` and `HCurveDao` exceptions are explicitly expected in the report.
- Scripts change both the handler source and other files in-place before invoking the prover; no valid snapshot equality between source of `HMaker.sol` now and the code actually transformed during a 2021 run has been established.

### Local execution evidence remains absent

The **real** checkout-based command `python scripts/check_specs.py .`, `python scripts/check_contests_csv.py .`, `python scripts/check_contracts.py .`, and `git -c core.whitespace=cr-at-eol diff --check origin/main...HEAD` were **not run** in this connector-only revision. The container's `git ls-remote` failed with `Could not resolve host: github.com`, the authorized Desktop Commander device is offline, and PR #8 has no GitHub Actions runs/checks to substitute. There are **no exit codes to report**. GitHub blob/content comparison and CVL bracket checks are review aids, not substitutes for a real checkout or Certora run.
