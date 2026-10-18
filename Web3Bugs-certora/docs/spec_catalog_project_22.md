# Project 22 — Popsicle V3 Optimizer (ECHO): inventory and semantic/soundness audit

## Historical provenance and scope
- Source: PropertyGPT/certora_projects/popsicle_v3_optimizer, PropertyGPT main SHA 687f654c679ed45ab127b7949e2a29c8f5e491b9.
- All 61 non-PDF original files, including exactly 54 Solidity .sol files, are preserved byte-for-byte in contracts/22. Original Solidity and original CVL were not modified. A per-project .gitattributes controls whitespace diagnostics on archived originals while preserving their bytes.
- PDF: resources/22/PopsicleV3OptimizerVerificationReport05Nov2021.pdf, SHA256 b11b2c428959dff60f5da03278868b804dcf844b1a23634dd725a09f37946298, 10 pages. Page-anchored Markdown extraction: reports/22.md. PDF remains the authoritative source.
- Official historical runner: contracts/22/spec/scripts/verifyPopsicleV3Optimizer.sh, linked target PopsicleV3Optimizer, DummyERC20A/B, SymbolicUniswapV3Pool and PoolVariablesWrapper, with solc7.6, --optimistic_loop, --loop_iter 1 and extensive verifier settings. The runner selects ONLY spec/PopsicleV3Optimizer.spec, with --rule $1.
- No archived runner selects FullMathWrapper.spec, PoolActions.spec or sanity.spec; corresponding target names are inferred from matching wrapper names and implementation, not falsely advertised as original executed commands.

## Complete declaration inventory and classification
- 4 specs, 21 active declarations: FullMathWrapper.spec 3 rules; PoolActions.spec 3 rules; PopsicleV3Optimizer.spec 9 invariants + 4 rules; sanity.spec 2 rules.
- Excluded commented declarations: FullMathWrapper.spec:41-57 integrityOfSafeMulDiv; PopsicleV3Optimizer.spec:299-321 more_shares_more_amounts_to_withdraw, :423-456 withdraw_amount, :458-463 zeroBalancesAfterRebalance and ghost/invariant text in :465-489 (the block comment starting at :465 remains UNTERMINATED through EOF); sanity.spec:25-31 reentrency. These are not active properties.
- Source methods, using bindings, ghost approximateSqrt (active on optimizer), and definition excludeCallback are included as needed. All copied CVL property blocks are byte-exact original substrings in N.spec.
- 19 complete, 2 incomplete. COMPLETE means dependency symbols available in the archived snapshot, NOT rerunnable proof or true property.
- 12 individual source-equivalent VERIFIED results on pages 7-10 of historical report, 9 NOT_STATED; 12 NO_FINDING and 9 NOT_STATED detection outcomes; 3 UNMAPPED diagnostic rules (PoolActions.checkBurnAllLiquidity, sanity, sanityForView).

| # | Original active declaration | Source | Status | Result | Detection Outcome | Label |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | integrityOfMulDivNoOverflow | FullMathWrapper.spec:2-19 | complete | NOT_STATED | NOT_STATED | L2 |
| 2 | integrityOfMulDiv | FullMathWrapper.spec:22-38 | complete | NOT_STATED | NOT_STATED | L2 |
| 3 | checkMulDivRoundingUp | FullMathWrapper.spec:60-72 | complete | NOT_STATED | NOT_STATED | L2 |
| 4 | checkBurnLiquidityShare | PoolActions.spec:10-25 | incomplete | NOT_STATED | NOT_STATED | S3-2 |
| 5 | checkBurnExactLiquidity | PoolActions.spec:29-45 | incomplete | NOT_STATED | NOT_STATED | S6-2 |
| 6 | checkBurnAllLiquidity | PoolActions.spec:47-52 | complete | NOT_STATED | NOT_STATED | UNMAPPED |
| 7 | balance_vs_protocol_Liquidity | PopsicleV3Optimizer.spec:96-117 | complete | VERIFIED | NO_FINDING | S6-4 |
| 8 | balance_contract_GE_protocolFees | PopsicleV3Optimizer.spec:124-147 | complete | VERIFIED | NO_FINDING | S6-4 |
| 9 | empty_pool_state | PopsicleV3Optimizer.spec:154-173 | complete | VERIFIED | NO_FINDING | S6-4 |
| 10 | empty_pool_state_reverse | PopsicleV3Optimizer.spec:181-204 | complete | VERIFIED | NO_FINDING | S6-4 |
| 11 | zero_totalSupply_zero_owed | PopsicleV3Optimizer.spec:208-213 | complete | VERIFIED | NO_FINDING | S6-4 |
| 12 | pool_balance_vs_owed | PopsicleV3Optimizer.spec:219-221 | complete | VERIFIED | NO_FINDING | S6-4 |
| 13 | zero_pool_balance_zero_owed | PopsicleV3Optimizer.spec:227-230 | complete | VERIFIED | NO_FINDING | S6-4 |
| 14 | total_vs_protocol_Fees | PopsicleV3Optimizer.spec:235-243 | complete | VERIFIED | NO_FINDING | S6-4 |
| 15 | liquidity_GE_poolBalance0 | PopsicleV3Optimizer.spec:250-268 | complete | VERIFIED | NO_FINDING | S6-4 |
| 16 | zeroCharacteristicOfWithdraw | PopsicleV3Optimizer.spec:280-293 | complete | NOT_STATED | NOT_STATED | S6-2 |
| 17 | totalSupply_vs_positionAmounts | PopsicleV3Optimizer.spec:326-346 | complete | VERIFIED | NO_FINDING | S6-4 |
| 18 | protocolFees_state | PopsicleV3Optimizer.spec:353-378 | complete | VERIFIED | NO_FINDING | S6-4 |
| 19 | empty_pool_zero_totalSupply | PopsicleV3Optimizer.spec:385-421 | complete | VERIFIED | NO_FINDING | S6-4 |
| 20 | sanity | sanity.spec:9-14 | complete | NOT_STATED | NOT_STATED | UNMAPPED |
| 21 | sanityForView | sanity.spec:17-22 | complete | NOT_STATED | NOT_STATED | UNMAPPED |

## Recursive dependency and missing-symbol evidence

1. PoolActions.checkBurnLiquidityShare cannot resolve CVL totalSupply() as an executable getter on PoolActionsWrapper. PoolActionsWrapper.sol:13 stores a NONPUBLIC uint256 totalSupply and does not implement totalSupply() as an ABI function; the PoolActions CVL methods block does not declare it. **incomplete** independently of Prover availability.
2. PoolActions.checkBurnExactLiquidity uses bare to in require at CVL line 35 but declares no to input or local variable. Its Solidity wrapper HAS an address to parameter, which does not bind this free CVL symbol. **incomplete**; do not repair the CVL.
3. FullMathWrapper exposes both callMulDiv and callMulDivRoundingUp implemented through FullMath.sol. Treat these as dependency-complete despite historical report explicitly excluding math libraries and lacking runner for them.
4. PoolActionsWrapper.checkBurnAllLiquidity has an actual wrapper/library call, but its only postcondition is COMMENTED; it is complete as an exploratory call, UNMAPPED as a bug oracle.
5. Optimizer uses accessible public lastCompoundLiquidity storage/getter (PopsicleV3Optimizer.sol:448) and position_Liquidity()/protocol_Liquidity() helper functions at :688-694. These must NOT be incorrectly marked missing. Its ERC20 inherited getters, linked dummy token methods, SymbolicUniswapV3Pool balance/owed/liquidity getters and PoolActions library are preserved.
6. A directed dependency closure through requireInvariant was generated for each invariant and rule. Named invariants have mutually recursive proof premises (e.g. balance_vs_protocol_Liquidity -> empty_pool_state -> balance_contract_GE_protocolFees -> empty_pool_state), so a checked box alone cannot demonstrate independently initialized, non-vacuous induction. No contradictory axioms are demonstrated. CVL uses NONDET for tick math, positions, ratio and external strategy functions, and sqrt is summarized through a free approximateSqrt ghost without a correctness axiom.
7. The historical Uniswap replacement is a deliberately simplified token/ratio/liquidity model, not deployed UniswapV3 correctness. Optimistic loop unrolling and one iteration limit narrow coverage. Solidity preserved modules and library chains exist, but this does not prove that every effective runtime behavior was modeled.
8. Distinguish CVL declarations at the target from Solidity helpers: a Solidity field without public getter is NOT a CVL methods implementation. Similarly, NONDET is an abstraction, not evidence of concrete math verification.

## Report comparison / result provenance
The historical PDF pp.5-10 describes simplified Uniswap and math, formulae, and the checked predicates. Pages 7-10 individually mark 3 optimizer rules (totalSupply_vs_positionAmounts, protocolFees_state, empty_pool_zero_totalSupply) and all 9 active optimizer invariants ✔. An unchecked zeroCharacteristicOfWithdraw is printed on PDF p.6, so NOT_STATED. The report checks more_shares_more_amounts_to_withdraw and withdraw_amount, but those rules are commented out in the archived active CVL, so there are NO new active property examples for them and their check marks are not applied elsewhere. FullMath, PoolActions and sanity rules are not independently checked in the PDF.

PDF pp.3-4 describes historical issues (high theft of yield, medium loss of yield, low deposit outside tick range, low rounding-loss shares, governance recommendations) and reports fixes. Their previous versions, solver run commands and direct CVL failure evidence are not bound to each declaration. A report-wide finding never automatically makes a math or optimizer property VIOLATED or FINDING. The latest ✓ result on named optimizer rules reflects the historically reported, simplified verification and is recorded independently of NO_FINDING.

## Second semantic pass: materially important differences
- The token1 comparison in balance_vs_protocol_Liquidity is commented and not verified by that invariant.
- total_vs_protocol_Fees literally checks totalFees0 > protocolFees0 OR both zero; not >= and not token1.
- liquidity_GE_poolBalance0 literally demands EQUALITY with modeled token0 unowed balance; the name GE is misleading.
- pool_balance_vs_owed and zero_pool_balance_zero_owed are one-direction/componentwise checks, not equality.
- totalSupply_vs_positionAmounts assumes lastCompoundLiquidity(e)==0 in the initial state. After an arbitrary f, subtraction posLiquidityAfter-compoundAfter may have precondition or underflow nuances. The getter and storage exist.
- protocolFees_state upper-bounds governance token0 holdings by ABSOLUTE protocol fee delta, not just increases; it excludes acceptGovernance and two callback selectors and special-cases withdraw.
- empty_pool_zero_totalSupply assumes its own starting equivalence and numerous requireInvariant premises; a successful report run is not a blanket global proof.
- FullMath math rules compare arithmetic formulas under heterogeneous bounds. integrityOfMulDiv has NO active denominator != 0 require; some checks can revert outside the modeled domain.
- PoolActions.checkBurnLiquidityShare ignores the declared to parameter when forwarding recipient: it passes e.msg.sender instead, and its wrapper's private totalSupply accessor is missing.
- sanity and sanityForView deliberately assert false to test reachability, not normative security. They are NOT historical VIOLATED findings.
- The report's untested full Uniswap math and optimization routines remain excluded even when dependency-complete wrapper code is archived.

## Validation, SHA and review
Automated extraction preserves original rule/invariant bodies, literal source and PDF bytes. All 21 declaration ranges checked for verbatim inclusion. Validator output and Git SHA are recorded in the PR after actual execution; no historical Certora Prover run, CVL2 migration, deep unbounded math proof or independent formal sanity replay is claimed.

## Lexical preservation warning
The original PopsicleV3Optimizer.spec contains an unterminated /* comment beginning at line 465 and running through end of file. This makes totalSupplyIntegrity at line 487 INACTIVE under comment-aware scanning; an ordinary regex scanner may falsely inflate the inventory from 21 to 22. The archive is preserved byte-identically rather than fixing historical CVL syntax. The original spec may not be directly parseable without a separate historically grounded migration, so a report checkmark is not interpreted as evidence that this exact snapshot was compiled. The generated N.spec retains only the selected literal property and its real dependencies; it does not fabricate this ghost/invariant.
