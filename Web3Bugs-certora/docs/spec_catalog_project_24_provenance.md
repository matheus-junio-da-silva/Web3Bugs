# Project 24 — historical provenance, audit and attribution limits

## Provenance and immutable upstream snapshot

| PDF role | Path | Pages | SHA-256 |
|---|---|---:|---|
| Wrong upstream OpenZeppelin PDF | contracts/24/final-report-3.pdf | 34 | 902081d47617e0b05a6fb1441ec5c6a10ac26f557767ce96cdfef3075fad835b |
| Correct Certora Rocket Joe PDF | resources/24/Certora_Formal_Verification_Report_Rocket_Joe.pdf | 21 | f223d83ad55ec79376126a18219c0f417b732fea7d53cf4a743738840cdd43b4 |

Original wrong PDF Git blob: 5827a074b64d5466b80b1df1696692bb8c4b6c8b.
Original PropertyGPT main commit: 687f654c679ed45ab127b7949e2a29c8f5e491b9; path certora_projects/rocket_joe.
Correct document: **Formal Verification Report for Rocket Joe**, Certora.
Original publisher PDF URL: https://certora.cdn.prismic.io/certora/3b96d4be-611f-488e-92dc-89d44f4c8669_TraderJoe.pdf
Publisher overview: https://www.certora.com/reports/traderjoe-report
Original period: January 13 to March 4, 2022; site listing dated March 3, 2022.
Last audited git commit: ef2ef30248661b5509c52ab30af9bd0fc07f6657, https://github.com/lfj-gg/rocket-joe/commit/ef2ef30248661b5509c52ab30af9bd0fc07f6657.

The source's original PDF is incorrect. No bytes of the existing contracts/24
archive were modified. We downloaded the correct PDF separately from Certora,
confirmed the exact first-page title, and counted its 21 pages with a PDF parser.
The correct PDF has a different SHA-256 from the wrong OpenZeppelin PDF.

## Compared with the actual audited Solidity revision

The following were compared by fetching the raw Solidity source at the exact
audited commit and diffing it against preserved contracts/24/contracts source:

| Contract | Equality | Code-level evidence |
|---|---|---|
| RocketJoeFactory.sol | Identical bytes | No changed lines |
| RocketJoeToken.sol | Identical bytes | No changed lines |
| LaunchEvent.sol | Different | Archived getIncentives returns 0 for issuer before pair creation, while audited code returns tokenIncentiveIssuerRefund. Archived _safeTransferAVAX checks address(this).balance minus _value against avaxReserve, while audited code checks only address(this).balance against avaxReserve. |
| RocketJoeStaking.sol | Different | Archived withdraw decreases totalJoeStaked before updating rewardDebt and transferring pending rJoe; audited withdraw moves decrementing totalJoeStaked after rewardDebt update and external rJoe transfer. |

Both differences can affect source-level behavior, especially reward accounting
and reentrant external calls. Byte identity of one contract (Factory or Token)
does not prove the whole LaunchEvent/Staking target/harness is identical.
The original Certora run was not reproduced.

## Result assignment policy

The official report includes checked conditions on its last audited source,
but the 164 extracted properties are bound to the archived (different) source
version and incomplete historical harness. The prior 53 individual VERIFIED
attributions have been replaced by NOT_STATED for the source instances,
rather than pretending the report is about the archived revision or
mislabeling them VIOLATED. That retraction is a source-specific inference
decision, not a finding about Certora's work.

Detection Outcome is independently NOT_STATED unless prior documentation
already establishes an ambiguity requiring INCONCLUSIVE. We do not create
FINDING claims from issue similarity; the seven manual findings remain
report-level cases in results/bugs.csv. Bug Labels categorize the literal
CVL intent, not the documented result, and UNMAPPED is allowed.

Selected additional mismatches: sources 2, 5, 7 differ in printed
relational preconditions/observations; source 147 tests >= where the PDF
prints ==; source 150 uses a different variable than the printed PDF;
source 163 has an explicit report qualification saying nonreversion
could not independently be proven; sources 12, 13, 152, 154 have
weaknesses in existential/relational witness construction.

The 164 rows of spec_catalog_project_24_evidence_matrix.csv enumerate
for each property its literal assertion, hypothesis for a counterexample
(not an observed Certora counterexample), original Solidity evidence,
official page and report excerpt (when available), source provenance,
Bug Label, Result and Detection Outcome with a reason.

## Audited assumptions and remaining limitations

The historical report assumes initialized LaunchEvent state, correct WAVAX,
nonmalicious external libraries and contemporary joe-core contracts.
Loops were limited to one iteration, and the _safeTransferAVAX
verification harness may miss reentrancy. Staking has setup/invariant
assumptions, a nonreversion limitation and timing weakenings.
Missing original CVL import ../helpers/erc20.spec and original symbolic
harness/third-party dependency closure remain unresolved in this snapshot.

No Prover run, exact audited harness reconstitution, runtime exploit,
or actual counterexample is asserted by this catalog correction.
A verified same-name condition does not by itself establish proof
for the PropertyGPT revision.
