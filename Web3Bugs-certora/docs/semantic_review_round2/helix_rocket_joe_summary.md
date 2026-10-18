# HELIX — independent final Rocket Joe review

**Snapshot reviewed:** PR #21, commit `bb739e54ed8a63d2621aaec871725cbde8df67dc`, branch `catalog/p24-boreal-rocket-joe`.
**Independent reviewer:** HELIX. **Scope:** examples 1–164, `results/spec/incomplete/24`.
**Scope of verdict:** documentary integrity; **no Certora Prover replay** and **no claim of verification of the PropertyGPT revision**.

## Verdict: BLOCKED

The source archive and conservative result attribution are defensible, but **six concrete Markdown/label inconsistencies** require correction in the Boreal branch before documentary merge. HELIX did not modify Boreal's catalog branch.

## Full matrix counts

| Decision | Count |
|---|---:|
| CONFIRMED | 153 |
| CORRECTION_REQUIRED | 6 |
| INCONCLUSIVE | 5 |
| **Total** | **164** |

The independent matrix `helix_rocket_joe_review.csv` enumerates all 164 source lines, active assertion(s), requires/requireInvariants, entrypoints, Solidity associations, proposed label, Result, Outcome, PDF pages, SHA checks, missing harness evidence and case disposition. CONFIRMED means the documentary reconstruction is aligned, **not** formally VERIFIED.

## Independently verified archival identity

- Correct Rocket Joe PDF: `resources/24/Certora_Formal_Verification_Report_Rocket_Joe.pdf`, **21 pages**, SHA-256 `f223d83ad55ec79376126a18219c0f417b732fea7d53cf4a743738840cdd43b4`. Page 1 names *Formal Verification Report for Rocket Joe* and lists last audited commit `ef2ef302`.
- Wrong upstream PDF: `contracts/24/final-report-3.pdf`, **34 pages**, SHA-256 `902081d47617e0b05a6fb1441ec5c6a10ac26f557767ce96cdfef3075fad835b`. Page 1 identifies **Formal Verification of OpenZeppelin**. This PDF cannot support Rocket Joe verification.
- Compared exact public Solidity bytes from audited commit `ef2ef30248661b5509c52ab30af9bd0fc07f6657` against PropertyGPT archive:
  - `RocketJoeFactory.sol` and `RocketJoeToken.sol`: exact bytes.
  - `LaunchEvent.sol`: historical archive `getIncentives` returns 0 before a pair exists for issuer; audited revision returns `tokenIncentiveIssuerRefund`. Archived `_safeTransferAVAX` checks `address(this).balance - _value >= avaxReserve`, whereas audited revision checks `address(this).balance >= avaxReserve`.
  - `RocketJoeStaking.sol`: archive decrements `totalJoeStaked` before updating `rewardDebt` and paying pending rJoe; audited revision decrements `totalJoeStaked` afterward.
- Complete Joe* mocks/third-party code and historical symbolic harness/drivers are not reconstructed. CVL import `../helpers/erc20.spec` is unavailable. Formula-name similarity is **not** equivalence of symbolic program.

## Per-instance identity controls

- **164/164** original CVL property spans match the historical source exactly and are embedded literally in the corresponding `N.spec`.
- **164/164** `N.sol` noncomment code lines appear in the original historical Solidity source.
- All 164 source examples are `incomplete`; `NOT_STATED` is appropriate for the preserved snapshot absent a proved source+harness+target match.
- Historical `VERIFIED` attribution retracted in **53** rows. These 53 retractions are conservative and defensible, not 53 contract failures.
- Historical results in this snapshot: 164 `NOT_STATED`. Outcomes: 161 `NOT_STATED`, three `INCONCLUSIVE` (IDs 151, 152, 154).
- The official report contains named rules and checked conditions on the **audited commit**, but 98 rows are not individually named and even same-name report rules do not prove the different source/harness. The original wrong PDF is not evidence.
- Additional source/PDF formula comparison not conclusively resolved for examples 2, 5, 7, 147 and 150 (see matrix); these are documentary attribution uncertainties rather than automatically contract defects.

## Required corrections

| Priority | Example | File | Finding |
|---|---:|---|---|
| P1 | 12 | `results/spec/incomplete/24/12.md` | Commented `pairBalanceOne > pairBalanceTwo` is represented as active |
| P0 | 152 | `results/spec/incomplete/24/152.md` | Commented minimum-interval assertion represented as active; stale body text says historical result is retained as VERIFIED despite Result NOT_STATED |
| P1 | 154 | `results/spec/incomplete/24/154.md` | Commented direct `rJoe2 > rJoe1` represented as active |
| P1 | 159 | `results/spec/incomplete/24/159.md` | Omitted fourth executable assertion `pendingRJoe(e,e.msg.sender) == 0` |
| P1 | 160 | `results/spec/incomplete/24/160.md` | Omitted fourth executable assertion `pendingRJoe(e,e.msg.sender) == 0` |
| P1 | 163 | `results/spec/incomplete/24/163.md` | Treats commented nonreversion assert as active. Source has `require lastReverted == false`; current S5-2 label is inconsistent with the two active principal-accounting assertions; propose S6-4 |

Review the existential implications in IDs 12, 13, 152 and 154 for vacuity before using them as substantive monotonicity/reward oracles. Do not infer a failing test from a weak specification. `sanity` (ID 164) has `assert false` as a reachability probe, appropriately UNMAPPED. The homonymous `hl_moreDepositMoreGet` at IDs 12 and 138 are different original rule bodies, not duplicates to collapse.

## Validator reproduction at exact SHA

Ran on read-only checker checkout of `bb739e54ed8a63d2621aaec871725cbde8df67dc`, using real repository root and `Web3Bugs-certora` directory:

- `cd Web3Bugs-certora && python3 scripts/check_specs.py .` → **exit 0**, 1,386 examples, 1,391 label relations.
- `cd Web3Bugs-certora && python3 scripts/check_contests_csv.py .` → **exit 0**.
- `cd Web3Bugs-certora && python3 scripts/check_contracts.py .` → **exit 0**.
- `git -c core.whitespace=cr-at-eol diff --check origin/main...HEAD` → **exit 0**; base SHA `80f551f23bbd86d7901c6a28e7f44c68aebae8fd`.

These are structural validators, not a soundness or Prover result. Initial checker invocation from the repository outer root failed to find `scripts/check_specs.py`; the successful commands used the actual `Web3Bugs-certora` root. A shallow checkout initially lacked a merge base; after fetching ancestry the required diff check passed.

## Conditions to move from BLOCKED to READY_FOR_DOCUMENTARY_MERGE

Correct the six `N.md` files above, align ID 163's Bug Label in any shared index/evidence CSV when justified by `docs/standard.md`, remove stale VERIFIED language from ID 152, rerun the four validators and request another independent review. No requirement for 164 reruns of Certora Prover is implied by the documentary-merge standard. Do not change the 164 `NOT_STATED` outcomes solely because the official report checked a similar condition at commit `ef2ef302`.
