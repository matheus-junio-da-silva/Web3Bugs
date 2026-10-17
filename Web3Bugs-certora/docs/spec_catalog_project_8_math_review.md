# Project 8 — AAVE Vault: satisfiability and semantic-impact register

This is an **independent mathematical review**, not a Certora Prover result. The historical PropertyGPT \`contracts/8/\` sources, specification axioms and Report PDF are unchanged.

## Arithmetic contradictions present in the original CVL

**W1 — universal ray multiplication**, in \`fees_LEQ_ATokenBal.spec:26–33\`, \`lastVaultBal_LEQ_ATokenBalThis.spec:20–27\` and \`positiveSupply_imply_positiveAssets.spec:29–36\`:

- The zero-input requirement imposes \(\mathrm{rayMul}_g(1,0)=0\).
- The simultaneous lower bound imposes \(1 \leq \mathrm{rayMul}_g(1,0)\).
- These formulae are inconsistent over ordinary integers, **independent of the Solidity target**. A model including them cannot satisfy the universal axiom.
- This is a *global axiom* in each originating specification, even for auxiliary invariants that do not call the ghost syntactically. Therefore every extracted proof environment retaining the originating axioms may be vacuous.

**W2 — zero-denominator multiplication**, in \`accrueYieldCheck.spec:11–21\`:

- For \(\mathrm{rounding}=0,\ x=y=\mathrm{denominator}=0\), the strict inequality becomes \(0 < 0\).
- Independently, the \(\mathrm{rounding}=1\) strict axiom cannot hold for \(\mathrm{denominator}=0\) with nonnegative \(\mathrm{x,y}\).
- No \(\mathrm{denominator}>0\) guard scopes these universal assertions in the visible original source.

**W3 — zero-denominator ray division**, in \`accrueYieldCheck.spec:29–31\`:

- With \(x=0,\ y=0\), the second axiom requires \(\mathrm{RAY}\cdot 0 - 0/2 < \mathrm{rayDiv}_g(0,0)\cdot 0\), also \(0 < 0\).
- This is an independent contradiction in the same specification. It is *not* proof that real Solidity ever divides by zero: it shows the **axiomatisation** is inconsistent.

## Implications for verification claims

A first-order theory with inconsistent axioms has no satisfying model; a solver may be able to discharge arbitrary assertions vacuously if it treats the axioms in the usual way. The analysis does **not** show which historical Certora run, configuration, rule, target, or later tool version incorporated a particular axiom. \`Result=VERIFIED\` remains a faithfully reported historical statement when Certora names that property, **not** an independently certified sound proof of the original source instance. Do not upgrade \`NOT_STATED\` or downgrade the documented historical outcome based on this exercise. The source assertions and axioms are kept literally unchanged.

**Certora sanity/prover execution:** unavailable. The supplied snapshot lacks the original harnesses, pinned OpenZeppelin/Aave packages, CVL version, model links, configurations and run commands; \`certoraRun\` is not present in the command environment and authorized Desktop Commander is offline.

**Actual independent run:** \`python /mnt/data/p08_review/axiom_witness.py\` with SymPy 1.14 and \`use_lra_theory=True\` returned UNSAT for W1 and concrete \`False\` for W2/W3. See \`docs/spec_catalog_project_8_sanity.log\`. A preliminary use of \`sympy.satisfiable\` without linear-real-arithmetic theory treated equalities/inequalities as propositional atoms and was insufficient; it was corrected before accepting the result. Neither this test nor a JavaScript consistency scan is a substitute for Certora.

## All 42 source instances — global-axiom exposure

| ID | Source property | Model exposure | Historical Result | Detection Outcome | Label |
|---:|---|---|---|---|---|
| 1 | `accrueYieldCheck` | W2 + W3 | VERIFIED | NO_FINDING | S3-2 |
| 2 | `changeInContractBalanceShouldCauseAccrual` | No contradictory axiom identified in the original extracted model | VERIFIED | NO_FINDING | S3-1 |
| 3 | `must_not_revert` | No contradictory axiom identified in the original extracted model | VIOLATED | ACCEPTED_BEHAVIOR | UNMAPPED |
| 4 | `must_not_revert_unless_large_input__convertToShares` | No contradictory axiom identified in the original extracted model | NOT_STATED | NOT_STATED | UNMAPPED |
| 5 | `must_not_revert_unless_large_input__convertToAssets` | No contradictory axiom identified in the original extracted model | NOT_STATED | NOT_STATED | UNMAPPED |
| 6 | `previewDeposit_amount_check` | No contradictory axiom identified in the original extracted model | VERIFIED | NO_FINDING | S6-2 |
| 7 | `previewDeposit_has_NO_threshold` | No contradictory axiom identified in the original extracted model | VIOLATED | ACCEPTED_BEHAVIOR | S6-2 |
| 8 | `previewMint_amount_check` | No contradictory axiom identified in the original extracted model | VERIFIED | NO_FINDING | S6-2 |
| 9 | `previewMint_has_NO_threshold` | No contradictory axiom identified in the original extracted model | VIOLATED | ACCEPTED_BEHAVIOR | S6-2 |
| 10 | `previewWithdraw_amount_check` | No contradictory axiom identified in the original extracted model | VERIFIED | NO_FINDING | S6-2 |
| 11 | `previewWithdraw_has_NO_threshold` | No contradictory axiom identified in the original extracted model | VIOLATED | ACCEPTED_BEHAVIOR | S6-2 |
| 12 | `previewRedeem_amount_check` | No contradictory axiom identified in the original extracted model | VERIFIED | NO_FINDING | S6-2 |
| 13 | `previewRedeem_has_NO_threshold` | No contradictory axiom identified in the original extracted model | VIOLATED | ACCEPTED_BEHAVIOR | S6-2 |
| 14 | `inv_sumAllBalance_eq_totalSupply__underline` | W1 | NOT_STATED | NOT_STATED | UNMAPPED |
| 15 | `inv_sumAllBalance_eq_totalSupply__atoken` | W1 | NOT_STATED | NOT_STATED | UNMAPPED |
| 16 | `inv_sumAllBalance_eq_totalSupply` | W1 | NOT_STATED | NOT_STATED | S6-4 |
| 17 | `lastVaultBalance_OK` | W1 | NOT_STATED | NOT_STATED | S6-4 |
| 18 | `getCLMFees_LEQ_ATokenBAL_DM_other` | W1 | NOT_STATED | NOT_STATED | S6-4 |
| 19 | `getCLMFees_LEQ_ATokenBAL_RW` | W1 | NOT_STATED | NOT_STATED | S6-4 |
| 20 | `inv_sumAllBalance_eq_totalSupply__underline` | W1 | NOT_STATED | NOT_STATED | UNMAPPED |
| 21 | `inv_sumAllBalance_eq_totalSupply__atoken` | W1 | NOT_STATED | NOT_STATED | UNMAPPED |
| 22 | `inv_sumAllBalance_eq_totalSupply` | W1 | NOT_STATED | NOT_STATED | S6-4 |
| 23 | `lastVaultBalance_LEQ_ATokenBalThis` | W1 | NOT_STATED | NOT_STATED | S6-4 |
| 24 | `inv_sumAllBalance_eq_totalSupply__underline` | W1 | NOT_STATED | NOT_STATED | UNMAPPED |
| 25 | `inv_sumAllBalance_eq_totalSupply__atoken` | W1 | NOT_STATED | NOT_STATED | UNMAPPED |
| 26 | `inv_sumAllBalance_eq_totalSupply` | W1 | NOT_STATED | NOT_STATED | S6-4 |
| 27 | `lastVaultBalance_OK` | W1 | NOT_STATED | NOT_STATED | S6-4 |
| 28 | `inv_fee_LEQ_ATokenBal` | W1 | NOT_STATED | NOT_STATED | S6-4 |
| 29 | `positiveSupply_imply_positiveAssets_all_deposit` | W1 | NOT_STATED | NOT_STATED | S6-4 |
| 30 | `positiveSupply_imply_positiveAssets_all_mint` | W1 | NOT_STATED | NOT_STATED | S6-4 |
| 31 | `positiveSupply_imply_positiveAssets_other` | W1 | NOT_STATED | NOT_STATED | S6-4 |
| 32 | `positiveSupply_imply_positiveAssets_specific_DM` | W1 | NOT_STATED | NOT_STATED | S6-4 |
| 33 | `positiveSupply_imply_positiveAssets_all_withdraw` | W1 | NOT_STATED | NOT_STATED | S6-4 |
| 34 | `positiveSupply_imply_positiveAssets_all_redeem` | W1 | NOT_STATED | NOT_STATED | S6-4 |
| 35 | `positiveSupply_imply_positiveAssets_specific_RW` | W1 | NOT_STATED | NOT_STATED | S6-4 |
| 36 | `rayMul_prop_1` | No contradictory axiom identified in the original extracted model | NOT_STATED | NOT_STATED | L2 |
| 37 | `rayMul_prop_2` | No contradictory axiom identified in the original extracted model | NOT_STATED | NOT_STATED | L2 |
| 38 | `mulDiv_properties` | No contradictory axiom identified in the original extracted model | NOT_STATED | NOT_STATED | L2 |
| 39 | `inv_sumAllBalance_eq_totalSupply` | No contradictory axiom identified in the original extracted model | NOT_STATED | NOT_STATED | S6-4 |
| 40 | `inv_balanceOf_leq_totalSupply` | No contradictory axiom identified in the original extracted model | NOT_STATED | NOT_STATED | S6-4 |
| 41 | `inv_sumAllBalance_eq_totalSupply__underline` | No contradictory axiom identified in the original extracted model | NOT_STATED | NOT_STATED | UNMAPPED |
| 42 | `inv_sumAllBalance_eq_totalSupply__atoken` | No contradictory axiom identified in the original extracted model | NOT_STATED | NOT_STATED | UNMAPPED |

**Scope:** W1 applies to **22** instances, IDs 14–35. W2 and W3 apply to **1**, ID 1. The other **19** instances have no contradiction of these particular forms identified; that does not establish their full global model satisfiable. No Prover model check has been run. The 42 `.txt` files document source-specific missing external implementations; the separate syntax-closure review retains ambient global axioms rather than silently removing them merely because the selected rule does not call the associated ghost.

**General non-vacuity caveat:** All `VERIFIED` statuses in this dataset should be interpreted with the report's assumptions, including single-step loop unrolling, symbolic tokens, fixed index ranges and absent full cryptography proofs. Result and Detection Outcome are distinct fields.
