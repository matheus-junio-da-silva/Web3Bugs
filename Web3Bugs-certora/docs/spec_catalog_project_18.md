# Project 18 — OpenZeppelin (historical PropertyGPT/openzepplin)

## Canonical provenance

- Source: `matheus-junio-da-silva/PropertyGPT@687f654c679ed45ab127b7949e2a29c8f5e491b9`, `certora_projects/openzepplin/`.
- Destination base: `matheus-junio-da-silva/Web3Bugs@46670617ee77649217b9dbf64fd6955344cedcf7`.
- Original report: `resources/18/OZ-final-report.pdf` (13 pages; May 9–June 10, 2022; report-reviewed commit `109778c`).
- Copy of 307 source files under `contracts/18` retains the original version byte-for-byte; no CVL2 migration.

## Coverage reconciliation

- 17 .spec files in source; 16 contain active properties. `erc20.spec` defines only reusable methods, with no standalone active rule/invariant.
- **168 original active rule/invariant declarations** across 16 specs. Three lines counted by a naive grep are nonactive/commented.
- **181 target-context examples:** the Initializable specification has 13 source declarations indexed separately for the two distinct flat and multi-inheritance harness contexts described by the PDF (26 entries). These 13 extra rows do not imply 13 additional original rules or independently proven per-target outcomes.
- Status summary: **69 complete** for *narrow source-availability cataloging*; **112 incomplete**, always with a reason file.
- `complete` is not semantic reproducibility: no original Prover invocation, external-summary/assumption reconstruction, injected bug execution, or ABI verification is claimed.

### Active declaration coverage by source (and target expansion)

| Original spec | Active declarations | Indexed target contexts |
| --- | ---: | ---: |
| `AccessControl.spec` | 4 | 4 |
| `ERC1155.spec` | 41 | 41 |
| `ERC1155Burnable.spec` | 6 | 6 |
| `ERC1155Pausable.spec` | 8 | 8 |
| `ERC1155Supply.spec` | 4 | 4 |
| `ERC20FlashMint.spec` | 1 | 1 |
| `ERC20Votes.spec` | 16 | 16 |
| `ERC20Wrapper.spec` | 9 | 9 |
| `ERC721Votes.spec` | 11 | 11 |
| `GovernorBase.spec` | 13 | 13 |
| `GovernorCountingSimple.spec` | 8 | 8 |
| `GovernorPreventLateQuorum.spec` | 11 | 11 |
| `Initializable.spec` | 13 | 26 |
| `RulesInProgress.spec` | 2 | 2 |
| `TimelockController.spec` | 20 | 20 |
| `sanity.spec` | 1 | 1 |
| `erc20.spec` | 0 | 0 |

## Report-specific evidence boundaries

The 13-page PDF explicitly focuses on Initializable, ERC1155 Burnable/Pausable/Supply and GovernorPreventLateQuorum, with earlier ERC1155 base work. It does not state per-rule current-build results for all 168 source declarations or all targets.
The report directly identifies four *historically broken* GovernorPreventLateQuorum rule names (PDF p. 2). Those are recorded as `VIOLATED` with `FINDING` scoped only to tested historical revisions; the report says fixes were made, and no current-head failure is claimed.
The zero-supply quorum case (p. 3) is qualified by a developer response. The issue with extra Timelock executors explicitly has **Rules Broken: None**. Neither can be assigned to an arbitrary Timelock or ERC20Votes rule.
Bug injections 1–7 (pp. 12–13) are deliberate mutants. They demonstrate sensitivity of identified rules, not seven production bugs. The report-wide summary does not prove each individual unmentioned token/extension/governor rule.
Graphical status symbols are not accurately representable through plain text extraction; preserve the PDF as authoritative and do not infer VERIFIED simply from source `STATUS - verified` comments.

## Historical harness and semantic blockers

- Initializable: two distinct harness modes, private-state visibility changes and synthetic versioned methods required; original exact verification harnesses not present.
- Governor: unavailable `ERC20VotesHarness`, `ERC721VotesHarness`, `GovernorPreventLateQuorumHarness`, modified visibility, `latestCastVoteCall`, modified `_castVote`, and stubbed `_execute` (PDF p. 10).
- ERC1155Supply: `exists_wrapper`, owner-only mint/burn wrappers, additional hooks/method accessibility (PDF p. 9).
- ERC20Votes/ERC721Votes: missing historical getter/selector exposure and checkpoint mechanics; modern superficially similar mocks do not prove equivalence.
- ERC20Wrapper/ERC20FlashMint: original summaries/underlying-token assumptions are not present as executable run configuration.
- `RulesInProgress.spec` and `sanity.spec`: active but unreported; preserve unfinished normative checks separately from reachability-oriented `sanity`, which is `UNMAPPED`.
- Source completeness concerns and historical assumptions are distinct from a mere missing compiler, CVL1/CVL2 migration, or Prover licensing. No tools were substituted.

## Cross-check and reproduction

- The source original CVL body for every row is preserved as an exact substring of its original `contracts/18/specs/*.spec` file.
- `docs/spec_catalog_project_18_evidence.json` records every source declaration and derived target-aware entry with line ranges, label and dependency blocker.
- Source code excerpts have exact file+line headers and are documentation, not independently compilable contracts.
- Validation results and HEAD hashes are recorded separately in the final validation log. Structural validators cannot establish formal soundness.
