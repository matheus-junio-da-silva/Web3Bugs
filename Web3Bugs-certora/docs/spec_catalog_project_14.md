# Project 14 — Opyn Gamma Protocol: Boreal Certora Catalog

## Original sources and coverage

- Historical report: OpynGammaDec2020.pdf (19 pages), October 5–December 28, 2020.
- Source: PropertyGPT/certora_projects/opyn_gamma_protocol/. Only its six top-level *.spec files declare active properties; scripts/harness contain Solidity, not additional CVL specs.
- Active property declarations: 34 ({'ControllerOrderOfOperations.spec': 1, 'MarginVault.spec': 13, 'NoBankruptcy.spec': 5, 'Privileged.spec': 1, 'ValidBalances.spec': 9, 'controller.spec': 5}). All property bodies are included as literal original substrings in their selected N.spec files.
- Dependency status: {'complete': 34}. These statuses are based on source import availability, not successful historical Certora proof reproduction.
- Report results: {'NOT_STATED': 15, 'VERIFIED': 19}; Detection Outcomes: {'NOT_STATED': 15, 'NO_FINDING': 12, 'FINDING': 7}.
- Snapshot integrity: 133 non-PDF source blobs copied byte-for-byte into contracts/14; PDF blob Git SHA-1 = 4953e29b51fc4d3982aeac6e043898b12884fde1.
- Original PDF is preserved in resources/14. reports/14.md is a text transcript; equations/diagrams in the PDF are authoritative.

## Historical target mapping

- ControllerOrderOfOperations.spec: target ControllerHarness via specs/scripts/runOrderOfOperations.sh; target source specs/harness/ControllerHarness.sol.
- MarginVault.spec: target MarginVaultHarness via specs/scripts/runMarginVault.sh; target source specs/harness/MarginVaultHarness.sol.
- NoBankruptcy.spec: target ControllerHarnessExtra via specs/scripts/runNoBankruptcy.sh; target source specs/harness/ControllerHarnessExtra.sol.
- Privileged.spec: target Whitelist via specs/scripts/runPrivilegedWhitelist.sh; target source contracts/core/Whitelist.sol.
- ValidBalances.spec: target ControllerHarness via specs/scripts/runValidBalances.sh; target source specs/harness/ControllerHarness.sol.
- controller.spec: target ControllerHarness via specs/scripts/runController.sh; target source specs/harness/ControllerHarness.sol.

## Report assumptions and limits

- MarginVault library was verified independently of Controller using a dedicated harness. Latest report ✔ is distinct from issues found in earlier code.
- Controller checks use at most two oTokens and one collateral asset; per-operation at most one vault; one short and long oToken of the same collateral; neither Controller nor MarginPool receives tokens.
- The historical run scripts use -assumeUnwindCond, bounded loop iteration (-b=3), selected solver flags including -useNonLinearArithmetic, and per-rule -rule or -t=300 as applicable; runOrderOfOperations specifies solc6.10.
- specs/scripts/applyHarnesses.sh rewrites Controller and MarginPool code for verification, including changes to getProceed/getExcessCollateral and safe-transfer calls. Snapshot source may not equal the mutated prover input. The script is preserved; its effects must be evaluated in a separate reproducibility pass.
- Link declarations, contract aliases, mocked tokens and symbolic method summaries constrain guarantees. A methods {} declaration is not evidence of a Solidity implementation, and a proved rule may be conditional or vacuous.
- Results are attributed individually only where a named source rule and report semantics can be confidently reconciled; aggregated ✔* does not prove all independent case variants.

## Critical semantic divergences

- orderOfOperations has a selector-ordered assert true branch and otherwise checks only vault collateral; PDF Property 18 has a broader commutativity claim. Result remains NOT_STATED.
- OtokenInVaultIsWhitelisted must not be inferred to establish whitelist membership from its name; inspect the actual assertion and its require assumptions. The actual CVL enforces a pre-to-post whitelist implication and matches PDF item 26, marked ✔. This is not a tautology.
- NoBankruptcy source contains five specialized pre-expiry/symbolic cases; PDF Property 19 is a general solvency formula, not a separate verifier outcome for each case. All five remain NOT_STATED.
- cantSettleUnexpiredVault uses sinvoke followed by assert false and can be sensitive to unreachable paths and harness assumptions. No report result is invented.
- The inverse add/remove and additive issues were historical findings, although the named latest MarginVault rules are marked ✔. Detection Outcome is not deduced from the formal Result.
- PDF high-severity Oracle/DoS findings are cataloged in results/bugs.csv as historical report findings, without claiming that the 34 active CVL declarations directly detected them.

## Property-by-property inventory

| # | Source | Property | Target | Dependency | Result | Outcome | Bug Label | Report link |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ControllerOrderOfOperations.spec | orderOfOperations | ControllerHarness | complete | NOT_STATED | NOT_STATED | S3-2 | Report Property 18, PDF p. 12 |
| 2 | MarginVault.spec | validVault | MarginVaultHarness | complete | VERIFIED | NO_FINDING | S3-2 | MarginVault Property 1.I, PDF p. 6 |
| 3 | MarginVault.spec | validEntityIndex | MarginVaultHarness | complete | VERIFIED | FINDING | S2-1 | MarginVault Property 1.II, PDF p. 6 |
| 4 | MarginVault.spec | changeToOneEntity | MarginVaultHarness | complete | VERIFIED | NO_FINDING | S3-2 | MarginVault Property 2, PDF p. 6 |
| 5 | MarginVault.spec | successOfAddCollateral | MarginVaultHarness | complete | VERIFIED | NO_FINDING | S3-2 | MarginVault Property 3, PDF p. 7 |
| 6 | MarginVault.spec | integrityOfAddCollateral | MarginVaultHarness | complete | VERIFIED | NO_FINDING | S6-4 | MarginVault Property 4, PDF p. 7 |
| 7 | MarginVault.spec | additiveAddCollateral | MarginVaultHarness | complete | VERIFIED | FINDING | S6-4 | MarginVault Property 5, PDF p. 7 |
| 8 | MarginVault.spec | inverseAddRemoveCollateral | MarginVaultHarness | complete | VERIFIED | FINDING | S6-4 | MarginVault Property 6, PDF p. 7 |
| 9 | MarginVault.spec | integrityOfAddShort | MarginVaultHarness | complete | VERIFIED | NO_FINDING | S6-4 | MarginVault Property 7, PDF p. 7 |
| 10 | MarginVault.spec | additiveAddShort | MarginVaultHarness | complete | VERIFIED | FINDING | S6-4 | MarginVault Property 8, PDF p. 7 |
| 11 | MarginVault.spec | inverseAddRemoveShort | MarginVaultHarness | complete | VERIFIED | FINDING | S6-4 | MarginVault Property 9, PDF p. 8 |
| 12 | MarginVault.spec | integrityOfAddLong | MarginVaultHarness | complete | VERIFIED | NO_FINDING | S6-4 | MarginVault Property 10, PDF p. 8 |
| 13 | MarginVault.spec | additiveAddLong | MarginVaultHarness | complete | VERIFIED | FINDING | S6-4 | MarginVault Property 11, PDF p. 8 |
| 14 | MarginVault.spec | inverseAddRemoveLong | MarginVaultHarness | complete | VERIFIED | FINDING | S6-4 | MarginVault Property 12, PDF p. 8 |
| 15 | NoBankruptcy.spec | putOptionsPreExpiryCase1StartingWithAllCases | ControllerHarnessExtra | complete | NOT_STATED | NOT_STATED | S6-4 | Controller Property 19 (general solvency), PDF p. 12; no case-specific proof result |
| 16 | NoBankruptcy.spec | putOptionsPreExpiryCase2StartingWithAllCases | ControllerHarnessExtra | complete | NOT_STATED | NOT_STATED | S6-4 | Controller Property 19 (general solvency), PDF p. 12; no case-specific proof result |
| 17 | NoBankruptcy.spec | putOptionsPreExpiryCase3StartingWithAllCases | ControllerHarnessExtra | complete | NOT_STATED | NOT_STATED | S6-4 | Controller Property 19 (general solvency), PDF p. 12; no case-specific proof result |
| 18 | NoBankruptcy.spec | callOptionsPreExpiry | ControllerHarnessExtra | complete | NOT_STATED | NOT_STATED | S6-4 | Controller Property 19 (general solvency), PDF p. 12; no case-specific proof result |
| 19 | NoBankruptcy.spec | putOptionsPreExpiryCase3StartingWithAllCasesNoCode | ControllerHarnessExtra | complete | NOT_STATED | NOT_STATED | UNMAPPED | Controller Property 19 (general solvency), PDF p. 12; no case-specific proof result |
| 20 | Privileged.spec | privilegedOperation | Whitelist | complete | VERIFIED | NO_FINDING | S5-3 | Report Property 24, PDF p. 15 |
| 21 | ValidBalances.spec | validState | ControllerHarness | complete | NOT_STATED | NOT_STATED | S3-2 | Report Property 13/16, PDF p. 10–11 |
| 22 | ValidBalances.spec | validBalanceTotalCollateral | ControllerHarness | complete | NOT_STATED | NOT_STATED | S6-4 | Report Property 14, PDF p. 10 |
| 23 | ValidBalances.spec | validBalanceTotalLong | ControllerHarness | complete | NOT_STATED | NOT_STATED | S6-4 | Report Property 15, PDF p. 11 |
| 24 | ValidBalances.spec | validBalanceTotalShort | ControllerHarness | complete | NOT_STATED | NOT_STATED | S6-4 | Report Property 16, PDF p. 11 |
| 25 | ValidBalances.spec | cantSettleUnexpiredVault | ControllerHarness | complete | NOT_STATED | NOT_STATED | S5-2 | No individually named report entry for the time-gated settleVault probe |
| 26 | ValidBalances.spec | validBalanceOfTheSystem | ControllerHarness | complete | NOT_STATED | NOT_STATED | S6-4 | Report Property 13, PDF p. 10 |
| 27 | ValidBalances.spec | onlyValidOtoken | ControllerHarness | complete | VERIFIED | NO_FINDING | S5-2 | Report Property 25, PDF p. 15 |
| 28 | ValidBalances.spec | OtokenInVaultIsWhitelisted | ControllerHarness | complete | VERIFIED | NO_FINDING | S3-2 | Report Property 26, PDF p. 15 |
| 29 | ValidBalances.spec | assetIsNotOtoken | ControllerHarness | complete | VERIFIED | NO_FINDING | S2-1 | Report Property 27, PDF p. 15 |
| 30 | controller.spec | settleVault | ControllerHarness | complete | NOT_STATED | NOT_STATED | S6-4 | Report Property 23, PDF p. 14 |
| 31 | controller.spec | redeem | ControllerHarness | complete | VERIFIED | NO_FINDING | S6-4 | Report Property 22, PDF p. 13 |
| 32 | controller.spec | onlyOneVaultModified | ControllerHarness | complete | VERIFIED | NO_FINDING | S3-2 | Report Property 17, PDF p. 11 |
| 33 | controller.spec | collateralWithdrawsRestricted | ControllerHarness | complete | NOT_STATED | NOT_STATED | S6-4 | Report Property 20, PDF p. 13 |
| 34 | controller.spec | optionWithdrawsRestricted | ControllerHarness | complete | NOT_STATED | NOT_STATED | S6-4 | Report Property 21, PDF p. 13 |

## Structural and semantic review

- Active declarations were scanned with comments removed, and declaration bodies were preserved literally in N.spec files.
- Every N.spec conservatively includes the source context outside excluded independent properties, including full source methods declarations and available helper functions; this is an over-approximation, not a minimal formally proven call-graph closure.
- Solidity excerpts carry file and exact line ranges; source text is literal. Per-example N.md specifies the target, report correspondence, actual conditional assertion, label rationale, and dependencies.
- Full historical Certora Prover replay is not claimed. It requires original compiler/verifier availability, harness transformations, symbolic configurations and satisfiability sanity checks.

## Review gate

- Official Python validators and git diff --check are required on the final commit. If not run or if any fail, the pull request must remain draft. Include actual exit codes and git commit SHA.
- No changes to Project 1–13 files are authorized.

## Harness versions and subsequent semantic corrections

- specs/harness/MarginVaultHarness.sol and specs/MarginVaultHarness.sol declare the same harness name but differ in the relative paths used for imported libraries. specs/scripts/runMarginVault.sh and specs/runMarginVault.sh select different copies, with differing flags and working-directory assumptions. Their historical prover environments must not be conflated.
- runNoBankruptcy.sh selects ControllerHarnessExtra, while runController.sh and runValidBalances.sh select ControllerHarness. Privileged.spec targets production Whitelist. The run scripts and applyHarnesses.sh are included in the immutable source snapshot.
- Example 27 onlyValidOtoken: PDF item 25 ✔, Result VERIFIED, Detection Outcome NO_FINDING; changes in pool balance or supply must imply whitelist approval under the rule preconditions.
- Example 28 OtokenInVaultIsWhitelisted: PDF item 26 ✔, Result VERIFIED, Detection Outcome NO_FINDING, technical label S3-2. Whitelist state is constrained before a modeled call and checked afterward. This is not a tautology.

## Formal validator execution record

The following commands were executed against the real checked-out and pushed Git head
fba323c1d70da86c670b9d4a4cdbac9b43e8a568 (base main 4a1bea89d88aa3b6aa165e8d81b8dd523c7afb82).
The host supplies Python 3 as python3; a private work-directory symlink named python points to that interpreter.
All commands were actually run, not simulated by an API structural check.

At Web3Bugs-certora/:

    python scripts/check_specs.py .
    Exit code: 0
    Check passed! 198 spec examples and 203 Bug Label relationships are structurally consistent.

    python scripts/check_contests_csv.py .
    Exit code: 0
    Check passed!
        ./results/contests.csv is consistant with ./reports

    python scripts/check_contracts.py .
    Exit code: 0
    Check passed!
        ./contracts is consistant with ./reports

At repository root:

    git -c core.whitespace=cr-at-eol diff --check origin/main...HEAD
    Exit code: 2
    624 whitespace warnings on 64 files. All identified warning categories are source-derived:
    129 in byte-identical historical contract/spec snapshot files, 495 in
    source-preserving extracted CVL/Solidity examples. No warnings were
    attributed to the generated Markdown report, catalog docs or CSV prose.

Representative actual git output:

    Web3Bugs-certora/contracts/14/specs/ControllerOrderOfOperations.spec:5: trailing whitespace.
    Web3Bugs-certora/contracts/14/specs/ControllerOrderOfOperations.spec:6: trailing whitespace.
    Web3Bugs-certora/contracts/14/specs/ControllerOrderOfOperations.spec:11: trailing whitespace.

The original source cannot be stripped of trailing whitespace while also keeping the
required byte-identical historical snapshot. The N.spec / N.sol excerpts likewise preserve
literal source lines, so whitespace from those excerpts remains. Do not present this
diff check as PASS. This is an outstanding review blocker and the PR must remain draft.
The orchestrator can either explicitly accept the original-source fidelity exception or
define a narrowly scoped policy for generated/source-derived files. No source CVL
expression was rewritten to suppress validation errors.

Independent source-level provenance audit after the commit:
- 34 catalog examples reconstructed from cited CVL source ranges byte-for-byte.
- 34 Solidity excerpts checked against original-file line ranges.
- 133 non-PDF files matched the PropertyGPT source byte-for-byte.
- OpynGammaDec2020.pdf Git blob SHA 4953e29b51fc4d3982aeac6e043898b12884fde1; 19 extracted report pages.
- Zero independent provenance discrepancies.

The three Python validators and the diff command will be repeated on the final PR head,
and the final tested SHA and exit codes will be recorded in the PR body.
