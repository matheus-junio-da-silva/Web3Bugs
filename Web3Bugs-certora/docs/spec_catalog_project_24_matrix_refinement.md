# Project 24 — refinement of the 164-property evidence matrix

## Scope and status

**DOCUMENTATION_FIX only; independent HELIX review pending.** The evidence
matrix retains one row per original CVL instance and has four new columns:

- **Preconditions and proof assumptions (source CVL):** literal require,
  requireInvariant, filtered selectors and storage-baseline assumptions.
- **Relevant state-changing calls (source CVL):** symbolic f(e,args)
  and named functions; invariants distinguished from one-off calls.
- **Read observations and getter bindings (source CVL):** before/after
  variables and original getters, not observed runtime results.
- **Specific falsification condition (hypothetical):** an explicit negation
  of the asserted relation or a specific violating state.

The existing hypothetical counterexample field now repeats the refined
scenario. Source CVL and Solidity excerpts remain immutable. These are
potential witnesses derived from syntax, NOT Prover-generated counterexamples.

## High-risk interpretation examples

- **10 (hl_whatShouldRevert):** when stopped() is true and f has selector
  depositAVAX, withdrawAVAX(uint256), createPair or withdrawLiquidity,
  execution of f@withrevert without reverting violates the implication.
  Other functions need not revert.
- **12–13:** existential dt implications permit vacuous witnesses and do
  not automatically imply monotonic incentive or penalty behavior.
- **147:** the preserved CVL requires joe.balanceOf(currentContract) >=
  totalJoeStaked(); a strictly smaller token balance falsifies it, whereas
  the historical report prints equality.
- **152, 154:** distinguish the direct positive-reward inequalities from
  existential time implications with possible vacuous witnesses.
- **163:** lastReverted == false is assumed after emergencyWithdraw@withrevert;
  the historical report expressly failed to prove nonreversion on its own.
- **164:** assert false is a reachability probe, not a reportable vulnerability.

## Change categories

| Category | Review decision |
|---|---|
| DOCUMENTATION_FIX | 164 matrix rows clarified, including all precondition and getter references. |
| LABEL_CHANGE | None in Rocket Joe; labels remain independent of formal outcomes. |
| RESULT_OUTCOME_CHANGE | None; 164 NOT_STATED results, 161 NOT_STATED and 3 INCONCLUSIVE detection outcomes. |
| DEPENDENCY_FIX | None; original CVL imports, symbolic harnesses and libraries remain incomplete. |
| EVIDENCE_GAP | Audited-source identity, harness reconstruction, Prover replay and independent HELIX review remain unavailable. |

## Provenance and gate

Correct Certora Rocket Joe PDF (21 pages):
https://certora.cdn.prismic.io/certora/3b96d4be-611f-488e-92dc-89d44f4c8669_TraderJoe.pdf

Preserved file: resources/24/Certora_Formal_Verification_Report_Rocket_Joe.pdf

SHA-256: f223d83ad55ec79376126a18219c0f417b732fea7d53cf4a743738840cdd43b4

The original 34-page OpenZeppelin PDF in contracts/24/final-report-3.pdf
remains byte-preserved and is NOT Rocket Joe verification evidence.
The audited Rocket Joe version differs from archived LaunchEvent and Staking.
Nothing here reinstates the previous 53 VERIFIED labels.

**PR #21 must remain Draft until HELIX's independent review and the
orchestrator's express approval. No merge.**
