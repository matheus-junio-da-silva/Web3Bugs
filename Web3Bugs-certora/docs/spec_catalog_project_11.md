# Project 11 — Helix: Keep Fully Backed Bonding specification catalog

## Sources and scope

- Original PropertyGPT tree: https://github.com/matheus-junio-da-silva/PropertyGPT/tree/main/certora_projects/keep_fully.
- Original 12-page PDF: `resources/11/KeepFullyBackedBondingNov2020.pdf`; page-based text transcription: `reports/11.md`.
- Certora report describes work undertaken 2–16 November 2020 on `FullyBackedBonding`, reviewed commit `658b02f237e25c370feaba80a7a3b13824190c4`. The snapshot is **not proven byte-identical** to that historical review commit.
- **Additional provenance cross-check:** the complete 46-file code/spec/harness subset (excluding PDF) is **46/46 Git blob SHA-1 identical** to upstream `keep-network/keep-ecdsa` branch `certora/fullybackedbonding-spec` at commit `a5cd1713621d94868765d1570fae373f4a497521`, under `solidity/`. The original report-reviewed commit `658b02f...` was not retrievable in that upstream repository, so this is source-branch identity, **not proof that this is the exact code exercised for every reported ✔**.
- Supplied spec: `contracts/11/specs/fullyBackedBonding.spec`; supplied auxiliary harnesses: `specs/harness/{Beneficiary,FullyBackedBondingHarness,OtherBeneficiary}.sol`. The original project has no run script or .conf.
- The target is cataloged as **FullyBackedBondingHarness**, inferred from used harness-only getters and variables. The report calls the verified production contract `FullyBackedBonding`; exact historical run target/linking is unconfirmed.

## Complete inventory and dependency status

- `fullyBackedBonding.spec`: **16 active properties** = **14 rules and 2 invariants**.
- Other spec files: 0. No commented-out `rule` or `invariant` is treated as active.
- 16 unique extracted examples and **16 spec_buglabel.csv relationships**; **0 complete, 16 incomplete**. All 16 use `results/spec/incomplete/11/N.{spec,sol,md,txt}`.
- The report's postponed cyclic authorization, inverse bond operations, exclusive-holder modification, deposit reachability/additivity/integrity and no-change-to-others concepts (items 5 and 16–21) are **not active source properties** and are not turned into examples.

**Missing dependency, evidence, and limitations.** The 47-file project snapshot contains the original CVL, three local harnesses, base contracts and inherited contract declarations, but does **not** vendor `@keep-network/keep-core/contracts/Authorizations.sol`, `StakeDelegatable.sol`, `KeepRegistry.sol`, `@keep-network/sortition-pools/contracts/api/IFullyBackedBonding.sol`, or `openzeppelin-solidity/contracts/math/SafeMath.sol`. Each runnable target is transitively dependent on these imports. A CVL `methods {}` declaration cannot substitute the real inherited implementation. Searched the complete `contracts/11/contracts/` and `contracts/11/specs/harness/` tree, including `api/`, `fully-backed/`, `test/`, `test/integration/`. No helper was imported from another project. Historical flags, package resolution, summaries and target linking are absent, so exact Prover reproduction cannot be claimed; lack of CVL2 migration alone did not cause incompleteness.

**Ghost / harness fidelity.** CVL `bondIDToOperator`, `totalLockedBonds`, `allLockedBond`, `allUnbonded`, `init_state`, Sload and Sstore hooks are extracted only when transitively needed. The harness overrides `getBondID` to consult `operatorHolderRefToBondID` and has `registerBondID`'s writes commented out; production `AbstractBonding.getBondID` instead hashes (operator, holder, referenceID). The snapshot therefore does not justify equating ghost tracked operator totals with production totals without a matching historical model. `everDeposited` and `balanceOf` are harness-only, not production Solidity getters.

## Formal results and audit outcomes

- **11 VERIFIED, 0 VIOLATED, 5 NOT_STATED**. Three separately named source conservation rules correspond to report item 6, a single aggregate `✔*` result; none inherits its individual verification status automatically. Additionally, `validState` and `noFrontRunningOnWithdraw` stay NOT_STATED due to material mismatches between the executable postcondition and the report's descriptive verified property.
- **10 NO_FINDING, 6 NOT_STATED, 0 FINDING per source rule**. The report's issue table does not name any of the 16 active source properties exactly as a broken detector. `validOperatorState`, cited for two invalid-parameter findings, has no exact active declaration. Outcome is not calculated from the formal status.
- Three report issues are listed in `results/bugs.csv`: zero operator, zero authorizer, and cyclic delegated authority (all labeled Low in the PDF). The cyclic issue is explicitly said to be impossible in the then-current version; its related proposed rule is postponed, not active. Its final finding classification is therefore conservatively O7 (doubtful/inapplicable for current implementation), **not SC as a proven exploitable implementation bug**. The catalog does **not** claim that these issue labels are the technical labels of a specific active assertion.
- Report marks `noBankruptcy`, user-can't-gain-assets and change-to-total-locked-bonds descriptions **✔***, i.e. proved under unspecified assumptions/simplified code. The report's total-assets-conservation aggregate is also **✔***, without individual exact source results. Remaining descriptive verified items are **✔**. The report does not provide sufficiently specific per-rule original summarization settings.
- The transitive `requireInvariant validOperator` in `validState` requires the `authorizerOf` declaration from source line 15. The independent dependency recheck caught and restored it before submitting the PR.
- The source comment beside `validState` says ❌ although the report's “Valid state of an Operator” is ✔; **source/report inconsistency preserved**, not silently reconciled. Its post-assertion only checks owner and beneficiary, while report prose additionally mentions authorizer.

## Bug Label audit

- 9 instances **S6-4** (asset conservation, deposit accounting, collateral obligations, withdrawal sums), 5 **S3-2** (operator state / ETH and bond ledger mutations), 1 **S2-1** (operator and authority address validation), 1 **UNMAPPED** (the front-running rule's unguarded second-withdraw revert oracle does not establish an SE-1 cause).
- **UNMAPPED: 1**. The single UNMAPPED case has normative independence intent but does not isolate its named front-running cause: an ordinary rejected withdrawal can falsify it even without interference. Other source assertions impose explicit normative invariants or transition equations. Labels describe the counterexample encoded by the assertion, not severity or reporting disposition. Multilabel rows: 0.
- The `noFrontRunningOnWithdraw` executable spec asserts the second scenario succeeds unconditionally, unlike report text implying equivalence between both withdrawals; it does not prove the stronger biconditional. Its `eWithdraw` may be unauthorized or underfunded and `succSceanrio1` is unused. Accordingly, the assertion cannot establish SE-1 on its own and the report's descriptive ✔ is not assigned to the source instance.
- `maximalWithdraw` only asserts zero balances if the chosen withdrawal succeeds; it does not prove every maximal withdrawal is callable.
- `assetsLessThanEverDepositedAsRule` has a post-call require that can filter changes; potential vacuity and the harness-only counter limit interpretation.

## Second semantic audit — every active source instance

Each row answers (a) what falsifies the assertion, (b) Bug Label justification, (c) normative/diagnostic, (d) unsupported report attribution, and (e) separation of detector / result / finding / target. All properties are *normative* and share the inferred harness target and absence of an exact finding linkage.

| Example | Exact rule/invariant | Counterexample to executable assertion | Defensible relationship | Report / interpretation boundary |
| --- | --- | --- | --- | --- |
| 1 | `validOperator` | Invalid zero operator or missing owner/authorizer with inconsistent beneficiary | S2-1: Nonzero operator ID, beneficiary and authorization identity invariant | Report broken rule is called validOperatorState, not this exact invariant. |
| 2 | `validState` | Operator retains tracked funds after owner or beneficiary disappears | S3-2: Accounted operator funds imply valid owner and beneficiary | **NOT_STATED**: source ❌ / report ✔ mismatch, source omits authorizer postcondition; seize branch is not restricted to the observed operator. |
| 3 | `noBankruptcy` | Global ledger liabilities exceed the contract Ether balance | S6-4: Aggregate tracked obligations do not exceed held ETH collateral | Report ✔*; assumptions/simplification unspecified. |
| 4 | `assetsLessThanEverDepositedAsRule` | Operator holdings exceed everDeposited | S6-4: Ever-deposited funds upper-bound operator holdings | Report ✔*; assumptions/simplification unspecified. |
| 5 | `totalAssetsPreserved` | Ordinary method changes operator holdings unexpectedly | S6-4: Operator asset conservation across ordinary calls | Report item 6 is aggregate ✔*; individual NOT_STATED. |
| 6 | `totalAssetsPreservedOnWithdraw` | Withdrawal fails to conserve funds plus beneficiary balance | S6-4: Withdraw conserves operator plus beneficiary ETH | Report item 6 is aggregate ✔*; individual NOT_STATED. |
| 7 | `totalAssetsPreservedOnSeizeBond` | Seizure does not conserve funds plus destination balance | S6-4: Seize conserves operator plus destination ETH | Report item 6 is aggregate ✔*; individual NOT_STATED. |
| 8 | `integrityOfWithdraw` | Withdraw mis-debits or mis-credits ETH | S6-4: Withdraw performs exact debits and beneficiary credit | Report-backed descriptive verified status; no exact finding linkage. |
| 9 | `maximalWithdraw` | Successful maximal withdraw leaves nonzero bonded or unbonded assets | S6-4: Successful maximal withdraw leaves no operator assets | Report-backed descriptive verified status; no exact finding linkage. |
| 10 | `additiveWithdraw` | Split and combined withdrawals diverge in success or balance | S6-4: Two withdrawals equal one combined withdrawal | Report-backed descriptive verified status; no exact finding linkage. |
| 11 | `noFrontRunningOnWithdraw` | Any second withdrawal revert, including unauthorized sender, insufficient unbonded amount or active delegation lock | **UNMAPPED**: no SE-1 causation established | **NOT_STATED**: report claims relational equivalence ✔, but executable assertion ignores baseline success and has unconstrained withdrawal environment. |
| 12 | `inverseOfDepositAndWithdraw` | Deposit followed by permitted withdraw fails to restore balances | S6-4: Depositing and withdrawing amount restores balances | Report-backed descriptive verified status; no exact finding linkage. |
| 13 | `validChangeToBalanceOf` | ETH balance changes via a method outside allowed payment flows | S3-2: Only supported operations may change user ETH balances | Report-backed descriptive verified status; no exact finding linkage. |
| 14 | `validChangeToTotalBondAmount` | Locked bond ledger updates in wrong direction or by excess | S3-2: Bond creation and release change locked totals in permitted directions | Report ✔*; harness bondID mapping assignment disabled. |
| 15 | `validChangeToUnbondedValue` | Unbonded ledger changes without matching operation and direction | S3-2: Unbonded values change only under permitted flows | Report-backed descriptive verified status; no exact finding linkage. |
| 16 | `validChangeToEverDeposited` | everDeposited changes outside deposit or by incorrect msg.value | S3-2: Historical deposit counter changes only with deposit-family methods | Report-backed descriptive verified status; no exact finding linkage. |

## Fidelity and preserved ambiguities

1. Different namespaces for report “validOperatorState” and source `validOperator`/`validState` prevent a forced FINDING relation.
2. Aggregate report item 6 lists 3 operational cases, but the source contains 3 separately named rules. All 3 remain NOT_STATED rather than propagating ✔*.
3. The report status ✔ for valid state contradicts the source's ❌ marker; its assertion does not require poststate authorizer nonzero even though report prose does. Its exact source rule is NOT_STATED, not automatically VERIFIED.
4. The report's “No front running” equivalence is stronger than the `succSceanrio2` check, which ignores `succSceanrio1`. The unrestricted withdrawal caller, amount and lock state create ordinary revert counterexamples. The original rule is preserved literally, but result/outcome are NOT_STATED and Bug Label is UNMAPPED.
5. CVL uses ghost hooks on harness tracking data; harness registerBondID lacks the actual storage mapping update and source-era types differ from modern CVL2. No migration or invented repair.
6. Seize conservation restricts destination to an OtherBeneficiary using-contract. `otherBeneficiary` as harness state name may not have identical semantics; historic linking is unknown.
7. The historical verified items are not claims of a rerun; ✔* restrictions, arbitrary method calls, call success assumptions and source-level `require` guards remain explicit.

## Source integrity

- Snapshot root: `contracts/11/` preserves all **47 blobs** from `certora_projects/keep_fully/`, including original PDF. An independent Git tree comparison found **47/47 identical Git blob SHA-1 values**, no mismatches; byte identity is assured by matching Git object identities.
- Source spec Git blob SHA-1: `5241b30db6e5781033c5ff422926477aa2bcb60a`.
- Original PDF Git blob SHA-1: `230fe69345766969b4038ca414a710c6aecadd20` (also reproduced at `resources/11/`).
- All sixteen extracted property blocks and cited Solidity line slices were compared as literal substrings of the copied original source at generation time and matched.
- Report transcript generated from original 12-page embedded PDF text layer; source PDF remains authoritative for visual layout and text-extraction ordering artifacts.

## Validation status

- **Generated and checked during extraction:** 16 active rule/invariant names, 16 source-property blocks, 16 sets of literal Solidity code slices, 64 artifacts, 47 Git blob source hashes.
- **Executed independently via GitHub API in JavaScript:** read-only structural replay of the three Python validator checks against branch tree, entire CSV and taxonomy, plus report and contract directory enumeration — **0 errors**, **185 relationship rows**, **180 unique examples**, **7 reports**, **7 contract project directories**, **0 orphan artifacts**; all 16 Project 11 rows resolve to four existing artifacts. This provides partial cross-checking but is not equivalent to running the original Python scripts.
- **Not executed:** `python scripts/check_specs.py .`, `python scripts/check_contests_csv.py .`, `python scripts/check_contracts.py .` and `git diff --check`. GitHub connector supports repository writes and reads but does not supply a local working checkout/terminal; the local container cannot resolve github.com. **No PASS is claimed.** An independent runner must execute these exact checks from `Web3Bugs-certora/` before merge.
- **CRLF / diff-check caution:** the two pre-existing shared CSV indexes use CRLF and were kept CRLF to preserve the dataset convention. A minimal local Git experiment confirms the default `git diff --check` can flag newly added CRLF lines as trailing whitespace (exit 2), while `git -c core.whitespace=cr-at-eol diff --check` passes for that *minimal test*. The exact target PR diff command was not executed and is **not** asserted to pass; the reviewer should inspect this environment-specific obstacle before merging.
- These structural checks cannot re-verify the old CVL proof or certify the semantic interpretation of assertions. The semantic review above separately addresses such limits.

## Catalog paths

- Index: `results/spec/spec_buglabel.csv`; artifacts: `results/spec/incomplete/11/`.
- Historical report: `reports/11.md`, original PDF: `resources/11/KeepFullyBackedBondingNov2020.pdf`.
- Snapshot: `contracts/11/`. Metadata: `results/contests.csv`. Report findings: `results/bugs.csv`.

## Adversarial review amendment

An independent follow-up review cross-checked all source assertions with the original report's status table, focusing on exact equivalence rather than similar titles. It changed the individual Result of `validState` and `noFrontRunningOnWithdraw` to NOT_STATED because the report's verified descriptions have materially different postconditions from the executable CVL. The latter also changed to UNMAPPED and NOT_STATED outcome because its failure can arise from ordinary access controls rather than an unexpected call sequence. Original `.spec` and source snapshot bytes remain unchanged. Report-level cyclic authorization was reclassified O7 in the findings CSV because the report itself says cycles cannot occur in the current implementation. See the affected examples' expanded semantic review.

### Per-example semantic corrections and scope caveats

- `validState`: source conditional seize path calls with unconstrained `seizeAddress`, not necessarily the operator whose post-state is observed. The source assertion omits poststate authorizer despite the report's descriptive predicate. Individual result remains NOT_STATED.
- `noFrontRunningOnWithdraw`: unrelated `f` is constrained to change some other-operator state but is **not** prohibited from also affecting the tested operator. The baseline success variable `succSceanrio1` is unused; `eWithdraw` is unconstrained, so a normal permission/lock/funding revert is an ordinary counterexample. Result/outcome NOT_STATED; Bug Label UNMAPPED rather than SE-1.
- `totalAssetsPreservedOnSeizeBond`: CVL uses a symbol from `using OtherBeneficiary`, whereas harness `otherBeneficiary` is a separately declared state variable. Missing historical link/initialization context may exclude successful seizures; this is documented as possible vacuity.
- `maximalWithdraw`: `everDeposited` tracks lifetime deposits, not current withdrawable funds; a revert of a maximal withdrawal satisfies its implication, so VERIFIED does not prove maximal withdrawals always succeed.
- `inverseOfDepositAndWithdraw`: report describes beneficiary transfer acceptance, but the CVL rule does not explicitly require this. The supplied Beneficiary harness is payable, but historical linkage to arbitrary beneficiaryOf addresses is unestablished.
- `validChangeToTotalBondAmount`: the `lockedBondsBefore + unbondedBefore` threshold lacks a local `safeAdd` requirement; no historical arithmetic fix is invented.
- Per-example `.txt` evidence now gives exact missing import sites (`FullyBackedBonding.sol:19-23`, `AbstractBonding.sol:19-21`) and separates ghost-model caveats from properties without ghost dependencies. The extracted CVL source remains byte-for-byte unchanged in its literal property bodies.


## Independent follow-up audit — 2026-10-17 UTC

This follow-up inspects the **existing Project 11 branch**, retaining historical source and all other projects unchanged. Its GitHub-readonly comparisons are substantive evidence but do not replace the official local validators or Certora Prover.

### Independently observed evidence (not an original-Prover rerun)

| Verification | Observed result | Method |
| --- | --- | --- |
| Original subtree integrity | MATCH | GitHub Contents API: source `certora_projects/keep_fully/` and destination `contracts/11/` have identical three root entries and identical Git blob/tree SHAs (`contracts/ = 29f8f200a81937574b6454a428f98798205a2ec0`, `specs/ = dbaa766df6fce096b722d2a9f81f7cdf8f635b85`, PDF blob `230fe69345766969b4038ca414a710c6aecadd20`). The extra resource PDF also matches. Matching subtree Git tree object IDs covers all children recursively. |
| Active original declarations | 14 rules, 2 invariants | Inspected top-level declarations in the historical `fullyBackedBonding.spec`. |
| Literal CVL property bodies | 16/16 MATCH | Compared each original named rule/invariant body against the corresponding `N.spec` body. Example 2 also includes the original `validOperator` invariant as a transitive dependency, not an extra separately cataloged source instance. |
| Solidity excerpt fidelity | 81/81 MATCH | Parsed every `// Extracted from` block and its cited line interval across all `N.sol`, then compared literal extracted text against the archived original `AbstractBonding.sol`, `FullyBackedBonding.sol`, and `FullyBackedBondingHarness.sol`. |
| Per-example metadata | 16/16 MATCH | Compared the 16 Project 11 CSV rows to the property heading, Result and Detection Outcome in the individual `N.md` files; no mismatch. |
| Target attribution | Inferred harness / reported production target remain distinct | No run configuration establishes that the original proof targeted the harness, although harness-only getters support the inference. |
| Dependencies | 16 incomplete; external package closure still absent | The original snapshot root matches; the included Solidity inherits/imports absent historical `@keep-network` and OpenZeppelin implementations. No `methods {}` signature is treated as an implementation. |
| Historic finding links | 3 report findings, 0 proved one-to-one source rule findings | The report cites `validOperatorState` rather than any exact active source rule for its two invalid-parameter issues; the cyclic-authorization discussion concerns a postponed property. |
| Report page-layout fidelity | **NOT VISUALLY VERIFIED** | The original PDF is preserved byte-identically and `reports/11.md` contains its 12 individually labeled text-layer pages; binary PDF rendering/screenshots were unavailable to this reviewer. Thus table placement, figure and continuation order are not certified. |

A further wording correction was committed to `results/spec/incomplete/11/11.md`: a revert in `noFrontRunningOnWithdraw` does **not** in itself establish *any* cross-operator sequence interference, let alone exploitable front-running. Its unguarded second success assertion is not a causal oracle.

### Official validator execution / environment blockers — actual observations

**No official PASS claim is made** for any of the four requested commands. The available local container has no cloned `Web3Bugs-certora/` working tree; `git ls-remote https://github.com/matheus-junio-da-silva/Web3Bugs.git refs/heads/catalog/p11-helix-keep-fully` returned:
```text
fatal: unable to access 'https://github.com/matheus-junio-da-silva/Web3Bugs.git/': Could not resolve host: github.com
```
The authorized Desktop Commander device was offline. GitHub's Actions API reported `{"total_count":0,"workflow_runs":[]}` for the branch at the time checked. Therefore, the exact branch versions of the following commands **remain blocked / not executed on a real checkout**:

```bash
cd Web3Bugs-certora
python scripts/check_specs.py .
python scripts/check_contests_csv.py .
python scripts/check_contracts.py .
git diff --check
```

Additional read-only PR patch inspection covered all **117** changed-file patches. No newly added line ended in space or tab. **17** added lines retained a CR byte at EOL (16 in `results/spec/spec_buglabel.csv`, 1 in `results/contests.csv`), preserving the pre-existing shared CSV format. A distinct **synthetic local Git test**, not the actual Project 11 checkout, gave `git diff --check` exit code **2** with CRLF addition (`trailing whitespace`), and `git -c core.whitespace=cr-at-eol diff --check` exit code **0**. This is supporting diagnosis of a probable default-check obstacle, **not** a PASS/FAIL log for the real branch. Do not normalize the shared CSVs or infer the exact branch command's exit status without running it.

The separate GitHub-readonly validations above do **not** constitute captured output of these four programs. The pre-existing CRLF-on-added-CSV warning still applies to the default `git diff --check`; its exact branch outcome must be recorded from a checkout rather than guessed. PDF visual inspection and original Prover reproduction likewise remain open prerequisites for approval. **Do not merge** until these are resolved by the orchestrator or a runner with repository access.
