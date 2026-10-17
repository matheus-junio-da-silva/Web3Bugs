# Project 9 — Celo Governance CVL catalog

**Agent:** Farol. **Scope:** exclusively PropertyGPT `certora_projects/celo_governance/` into Web3Bugs-certora. **Branch:** `catalog/p09-farol-celo-governance`. **Status:** historical catalog staged for **independent draft review**, with explicit historical dependencies and execution limitations.

## Input provenance and file integrity

- Read-only PropertyGPT repository: https://github.com/matheus-junio-da-silva/PropertyGPT/tree/main/certora_projects/celo_governance
- Source `main` revision observed while copying: `687f654c679ed45ab127b7949e2a29c8f5e491b9`.
- Source subtree Git hashes: `contracts/` = `7a4ccd3a239eb864cc1ab5c9af1d3b1916556f12`; `specs/` = `7eb91380b9da9b7a34bd0c64b9fc5a38edb2a9f6`.
- `contracts/9/contracts/` and `contracts/9/specs/`: **195 source blobs** (170 contract-tree files, 25 spec-tree files) copied without editing. All 195 destination blob hashes were compared against the corresponding source blobs and matched. Historical source SPDX notices/comments and odd spellings were not modified.
- `resources/9/CeloMay2020.pdf` is a byte-identical copy of the source PDF (Git blob SHA-1 `9801e32b8a0e59fe7dc7a0a11d736d1750c282e0`, 240,844 bytes).
- `reports/9.md` is currently a **faithful topical index, not a full-page verbatim transcript**. The authoritative original report, including its formulae and tables, is preserved in `resources/9/CeloMay2020.pdf`. A complete Markdown transcription is an **open quality task**, not silently claimed as done.
- Original Certora PDF: https://github.com/matheus-junio-da-silva/PropertyGPT/blob/main/certora_projects/celo_governance/CeloMay2020.pdf. The report cites two monitored code revisions, `9d2ec0d9399a6959565062f57efa037d03fd4fbc` (phase 1) and `a46ce55ebd3867fa69290bf3be040846d433525d` (phase 2). Those hashes are **not** automatically assigned to the supplied source snapshot.

## Inventory / counts

All `rule` and `invariant` declarations were enumerated after masking `//` and `/*...*/` comments; identical names in different files were kept as distinct instances. The active `rule address_cant_be_both_authorizedby_of_two_address`-looking text in `accounts.spec:72-90` is actually within a block comment opened at line 71 and closed at line 91: **excluded**, not silently counted. The 3 active rules in `governance_old_rules.spec` remain included despite the file name and its warning `Requires correction`.

| Source spec | Active properties | complete | incomplete |
| --- | ---: | ---: | ---: |
| `accounts.spec` | 25 | 25 | 0 |
| `accountsPrivileged.spec` | 1 | 1 | 0 |
| `goverance_with_dequeue.spec` | 3 | 2 | 1 |
| `governance-referendumVotes.spec` | 1 | 0 | 1 |
| `governance.spec` | 16 | 16 | 0 |
| `governancePrivileged.spec` | 1 | 1 | 0 |
| `governance_old_rules.spec` | 3 | 0 | 3 |
| `lockedGold.spec` | 7 | 7 | 0 |
| `locked_gold_linked.spec` | 3 | 0 | 3 |
| `reserve.spec` | 1 | 0 | 1 |
| **Total** | **61** | **52** | **9** |

- `61` distinct `Project ID=9` property rows in `results/spec/spec_buglabel.csv`; `61` distinct example IDs 1–61; each example uses one technically justified classification, including `UNMAPPED`.
- `52` complete triples (`.spec`, `.sol`, `.md`) and `9` incomplete quadruples (also `.txt`): **192** generated example artifacts. No `.txt` for complete.
- `4` `UNMAPPED` examples: `11:viewFunctionsDoNotRevert`, `20:check_no_fallback`, `27:may_dequeue`, `50:constitution_change_legal`.
- All 61 individual `Result` fields are `NOT_STATED` and all 61 `Detection Outcome` fields are `NOT_STATED`, rather than inheriting the report's aggregate assertion of verification. No source rule is independently identified by name, complete target context, and individual result in the preserved 2020 final report.

## Formal report outcomes, findings and attribution

The PDF says the protocol was verified with respect to the written high-level rules after fixes and presents **seven** historical findings in Table 1 (three High, four Low): invalid neighbor arguments to SortedLinkedList insertion; vote-unit rounding/front-running in Election; omission of pending LockedGold withdrawals in ReleaseGold's total balance; inappropriate election group reward state; redundant Election subtraction; unused LockedGold structures; and FixidityLib multiplication precision. The seven report findings are recorded separately in `results/bugs.csv`; their technical Web3Bugs labels are dataset classifications, **not** labels printed by Certora. None can be imputed as the result or reported finding of an unrelated extracted Accounts/Governance/Reserve rule merely from a similar state variable or high-level thematic overlap. The LockedGold **dead-code** issue is not a violation of `totalPreserved`, `withdraw`, or `noWithdrawBeforeUnlocking`.

The report's checked high-level properties, with their check marks, do not provide a name-by-name map to this later/divergent source snapshot. A high-level equivalent (e.g. persistent authorizedBy or LockedGold conservation) does not justify propagating `VERIFIED` to every variant with differing harnesses, assumptions, or quantification. `NOT_STATED` here means **not individually stated**, not `VIOLATED` and not proof of a security issue.

## Missing historical dependency / linkage audit

| Example | Missing or unestablished requirement | Locations inspected and implications |
| --- | --- | --- |
| 27 — `may_dequeue` | `callArbitrary(f)` is used without a declaration/import in `goverance_with_dequeue.spec`; a helper with that name appears only in sibling `governance.spec:386-390`. | No run script/linkage for this standalone variant; did not silently import the sibling helper. |
| 30 — `referendumVotesAreConsistent` | `requireInvariant referendumVoteIDIsLessThanOrEqCounter(v)` names an invariant absent locally; `governance.spec:211` has a **two-argument** invariant. | No import/run target establishes the one-argument signature. The local `votedFor` ghost and Sstore/Sload hooks are preserved; ghost initialization also quantifies `address p` where the ghost's second formal parameter is `uint256`, a possible historical typing inconsistency. |
| 48 — `no_double_vote_referendum_vote` | References `accounts.voteSignerToAccount`, without local `using Accounts as accounts` or import. | This alias appears only in `governance.spec:1`; no runner links the old file to it. |
| 49 — `sum_of_votes_cannot_exceed_total_weight` | Uses undeclared `callArbitrary(f)`, requiring unestablished linkage to helper/runner. | The rule itself also says the proof requires linked LockedGold; no historical linked run for this old variant is present. |
| 50 — `constitution_change_legal` | Uses undeclared `callArbitrary(f)`, with no historic runner. | Constitution legality assertions are **commented out**; only `assert true` is active. Correctness of the original intention is neither repaired nor claimed. |
| 58 — `no_validate_delegation_when_validating` | Historical `_isValidating` and `delegateValidating` calls lack an established implementation/linked harness. | Checked Accounts, Governance, LockedGold, harnesses/scripts; no `locked_gold_linked.spec` runner. |
| 59 — `no_vote_delegation_when_voting` | `delegateVoting` implementation and historic linkage missing. | `Governance.isVoting` exists, but does not supply missing delegation entrypoint or target wiring. |
| 60 — `no_weight_changing_when_voting` | `_weight` and `isVoting` lack the historical external call/linked target context for this standalone file. | Governance contains related internal computation, but there is no verified ABI or linked harness establishing the intended invocation. |
| 61 — `nonspenderCantReduceBalance` | **Concrete missing Solidity file**: `specs/harnesses/ReserveHarness.sol` imports `contracts/stability/Reserve.sol`, absent from the supplied complete contracts subtree. | The script `specs/scripts/reserve.sh` targets `ReserveHarness` and links Registry; a `MockReserve.sol` elsewhere is not a faithful replacement for the missing actual implementation. |

Each incomplete example carries `N.txt` with the original symbol/line, search path and reason. `complete` means locally closed symbolic dependencies in available source, **not** that a historical prover run would compile with today's CVL or exactly reproduce 2019–2020 results.

## Historical execution restrictions / source drift

- `accounts.sh` and `accountsPrivileged.sh` verify `AccountsHarness` using `--optimistic_loop --loop_iter 2`.
- `governance.sh` and `governancePrivileged.sh` verify `GovernanceHarness` and include `contracts/common/Accounts.sol`, also using `--optimistic_loop`. `using Accounts as accounts` is material to those rules, unlike unlinked old variants.
- `lockedgold.sh` links `LockedGoldHarness:goldToken=GoldTokenHarness`, enabling a modeled GoldToken interaction and using optimistic loop handling. Historical `lockedGold.spec` comments also show `-b=3,-assumeUnwindCond` with a bounded-loop setup. `getTotalPendingWithdrawals` is a loop over pending entries; `totalPreserved` and `noChangeByOther` require withdrawal-array length at most one.
- `reserve.sh` tries to verify `ReserveHarness` with Registry linkage, but the required Reserve.sol import is missing from the snapshot.
- `GovernanceHarness.dequeueProposalsIfReady()` is a **no-op override**, so rules depending on dequeuing may be vacuous in that harness even if their CVL dependencies are present.
- `specs/scripts/applyHarness.sh` edits local compiler input before verification: replaces `private` with `internal` in Governance, simplifies `FixidityLib.multiply`, changes `_isProposalPassing` to compare yes > no, and substitutes a successful synthetic external-call helper in Proposals. These transformations are **not** in the immutable copied original snapshot and are not evidence of equivalence for the deployed contract.
- `AccountsHarness` exposes `authorizedBy`, role/signer mappings and key lengths through extra public getters. `LockedGoldHarness.ercBalanceOf(address)` reads an EVM address's native balance, and the extracted `withdraw` rule explicitly tests the Prover's model of GoldToken._transfer, not a generic ERC20 ERC-balance theorem.
- CVL1/Specify parser/version, npm `openzeppelin-solidity` imports, missing historical run flags and multi-contract harness linkage may block precise reproduction even for `complete` cases. No helper is fabricated or transplanted from another project.

## Second semantic audit — per-example falsifier, classification and limits

For every row below: **(a)** the last column describes the security/consistency condition whose falsification under its `require` premises would give a counterexample; **(b)** the `Bug Label` denotes the assertion's actual counterexample type (or `UNMAPPED`); **(c)** the diagnostic column distinguishes a normative property from exploration/model checking; **(d)** the final 2020 report states no individual outcome for this exact source instance (therefore no `FINDING`, `VERIFIED`, or `ACCEPTED_BEHAVIOR` is inferred); **(e)** the source+line column and each corresponding `N.md` record the concrete target/harness and preserve variant boundaries. `C` = dependency-complete, `I` = incomplete. The text is reconstructed from the literal CVL assertion, not from private auditor thought.

| ID | Source instance and literal Property | Status | Bug Label | Normative / diagnostic | Condition tested / falsification and caveat |
| ---: | --- | :---: | --- | --- | --- |
| 1 | `accounts.spec:35-40` / `account_empty_if_not_exist` | C | `S3-2` | Normative | An unregistered address must not have a wallet or signer recorded. |
| 2 | `accounts.spec:46-48` / `address_cant_be_both_account_and_signer` | C | `S2-1` | Normative | A signer authorized by a separate account must not simultaneously be an account. |
| 3 | `accounts.spec:54-57` / `address_signer_if_authorizedby_legacy` | C | `S3-2` | Normative | An authorized legacy signer must point back to the correct account. |
| 4 | `accounts.spec:62-65` / `address_signer_if_authroizedby_new` | C | `S3-2` | Normative | A default-role signer must point back to the correct authorizing account. |
| 5 | `accounts.spec:96-120` / `address_can_authorize_two_addresses_legacy` | C | `S3-2` | Normative | Starting a validator signer and authorizing a distinct vote signer must not displace the first authorization. |
| 6 | `accounts.spec:125-149` / `address_can_authorize_two_addresses` | C | `S3-2` | Normative | Two authorizations in distinct roles must preserve both authorizedBy pointers. |
| 7 | `accounts.spec:154-162` / `authorizedBy_can_not_be_removed` | C | `S3-2` | Normative | A nonzero authorizedBy pointer must survive arbitrary state-changing methods. |
| 8 | `accounts.spec:167-176` / `initializableOnlyOnce` | C | `S5-2` | Normative | Initialize must revert on its second invocation. |
| 9 | `accounts.spec:181-191` / `createsAccount` | C | `S3-2` | Normative | The rule excludes createAccount/setAccount and asks whether another function changes isAccount; no caller identity is checked, so this is unexpected state mutation, not a proof of … |
| 10 | `accounts.spec:196-197` / `legacyRolesAreNotUsedInNewRoles` | C | `S3-2` | Normative | Legacy roles must not be populated in the generic default-signers mapping. |
| 11 | `accounts.spec:203-258` / `viewFunctionsDoNotRevert` | C | `UNMAPPED` | Diagnostic / partial | Selected view methods must not revert under explicitly constrained call contexts. — Filtered view no-revert probe; specially excluded selectors and role premises. |
| 12 | `accounts.spec:263-264` / `authorizedByIsNeverReflexive` | C | `S2-1` | Normative | An address must not authorize itself. |
| 13 | `accounts.spec:270-271` / `mustHaveAuthorizedByIfCompletedSignerAuthorization` | C | `S3-1` | Normative | Completion of a signer authorization must update the signer's authorizedBy pointer. |
| 14 | `accounts.spec:276-285` / `noMultipleAccountsPerSignerInARole` | C | `S2-3` | Normative | One signer must not be completed as a signer for two distinct accounts. |
| 15 | `accounts.spec:290-303` / `cantGoFromNoAuthorizationToCompletedInOneStepUnlessRoleIsLegacy` | C | `S5-2` | Normative | Nonlegacy signer authorization must not become completed without a started phase, unless invoking the explicitly excluded signature helper. |
| 16 | `accounts.spec:309-330` / `cantMakeASignerForNonLegacyRoleWithoutApprovalOfSigner` | C | `S5-3` | Normative | A nonlegacy signer must personally authorize completion unless using the excluded signature method. |
| 17 | `accounts.spec:335-346` / `cannotStartSignerAuthorizationsForOtherAccounts` | C | `S5-3` | Normative | A transaction cannot start authorization for an account other than msg.sender. |
| 18 | `accounts.spec:351-368` / `cannotSetAuthorizedByWithoutSignatures` | C | `S5-3` | Normative | A zero authorizedBy pointer must not be set by an unauthorized caller outside the listed signature paths. |
| 19 | `accounts.spec:373-388` / `signerAuthorizationChangePrivileges` | C | `S5-1` | Normative | Starting/completing/revoking signer authorizations must obey the respective account/signer caller restrictions. |
| 20 | `accounts.spec:393-399` / `check_no_fallback` | C | `UNMAPPED` | Diagnostic / partial | The source diagnostic checks fallback behavior by requiring a revert; no explicit high-level vulnerability class is isolated. — Fallback nonexistence/revert sanity check. |
| 21 | `accounts.spec:404-431` / `gettersInAgreement` | C | `S6-2` | Normative | The different signer getters must agree; the preserved source also unconditionally asserts all getter values are nonzero. |
| 22 | `accounts.spec:436-442` / `accountToSignerAndInverseVote` | C | `S6-2` | Normative | Vote role signer-to-account and account-to-signer lookup must agree. |
| 23 | `accounts.spec:444-450` / `accountToSignerAndInverseValidator` | C | `S6-2` | Normative | Validator role signer-to-account and account-to-signer lookup must agree. |
| 24 | `accounts.spec:452-458` / `accountToSignerAndInverseAttestation` | C | `S6-2` | Normative | Attestation role signer-to-account and account-to-signer lookup must agree. |
| 25 | `accounts.spec:460-466` / `accountToSignerAndInverseNewRoles` | C | `S6-2` | Normative | The new-role indexed signer must map back to the expected account. |
| 26 | `accountsPrivileged.spec:31-50` / `privilegedOperation` | C | `S5-3` | Diagnostic / partial | The same selected operation must not succeed from two distinct caller identities when treated as privileged. This does not identify which caller is authorized. — Partial two-caller access-control detector, not proof of authorized identity. |
| 27 | `goverance_with_dequeue.spec:2-17` / `may_dequeue` | I | `UNMAPPED` | Diagnostic / partial | This exploratory rule probes whether an arbitrary non-view function can fill an initially empty dequeue-array index; it does not exclude legitimate promotion/dequeue calls or indep… — Exploratory arbitrary-method dequeue mutation; legitimate promotion not excluded. |
| 28 | `goverance_with_dequeue.spec:19-49` / `promote_proposal` | C | `S5-2` | Normative | A promoted proposal must not exceed the queue-expiry time boundary. |
| 29 | `goverance_with_dequeue.spec:55-74` / `no_promoting_without_upvotes` | C | `S5-2` | Normative | A proposal cannot be promoted into the dequeued array without previously receiving upvotes. — GovernanceHarness overrides dequeueProposalsIfReady as a no-op: possible vacuity. |
| 30 | `governance-referendumVotes.spec:23-28` / `referendumVotesAreConsistent` | I | `S3-2` | Normative | Recorded referendum proposal IDs must agree with the votedFor tracking ghost whenever the proposal exists. — One-argument requireInvariant refers to a two-argument sibling signature. |
| 31 | `governance.spec:58-59` / `dequeuedIsWithinRange` | C | `S2-1` | Normative | Dequeued entries must not reference proposal IDs beyond the proposal counter. |
| 32 | `governance.spec:62-74` / `upvotesConsistency` | C | `S3-2` | Normative | Upvote-record changes must preserve the encoded record-structure invariant. |
| 33 | `governance.spec:80-97` / `no_double_upvote` | C | `S6-4` | Normative | A second upvote from a previously upvoting account must not increase that proposal's upvote total. |
| 34 | `governance.spec:99-114` / `proposal_count_monotonic_increasing` | C | `S3-1` | Normative | Successful proposal creation must increment proposalCount, while other successful actions must not decrease it. |
| 35 | `governance.spec:118-141` / `no_referendum_votes_unless_approved` | C | `S5-2` | Normative | No initial referendum vote totals may become positive unless the proposal was already approved. |
| 36 | `governance.spec:143-161` / `cant_unvote` | C | `S5-2` | Normative | Voting with the special None option cannot change a previous vote record or weight. |
| 37 | `governance.spec:164-209` / `no_double_vote_referendum_all_but_vote` | C | `S6-4` | Normative | Operations other than vote and revokeVotes must not illegitimately inflate/rewrite the recorded proposal vote totals. |
| 38 | `governance.spec:211-215` / `referendumVoteIDIsLessThanOrEqCounter` | C | `S2-1` | Normative | Ghost-recorded referendum proposal IDs must not exceed the proposal counter. |
| 39 | `governance.spec:218-241` / `approval_only_if_promoted_and_allowed` | C | `S5-3` | Normative | New approval requires dequeued presence and the documented approver identity. |
| 40 | `governance.spec:244-268` / `approved_proposals_invariants` | C | `S3-2` | Normative | Approval must not result in nonexistent proposals or be reversed while a proposal still exists. |
| 41 | `governance.spec:271-287` / `execute_preconds` | C | `S5-2` | Normative | Execution must not succeed when NO votes are at least YES votes. |
| 42 | `governance.spec:291-309` / `modifying_stageDuration` | C | `S3-2` | Normative | The rule tests unauthorized mutation by method selector, excluding the known duration setters and initializer; it does not restrict msg.sender and cannot by itself prove a caller-a… |
| 43 | `governance.spec:311-323` / `can_add_to_queue` | C | `S3-2` | Normative | Other operations may not increase queue length; the rule intentionally exempts propose. |
| 44 | `governance.spec:325-347` / `constitution_change` | C | `S3-2` | Normative | The rule excludes setConstitution by selector and checks that other methods preserve the getter value, not that a particular caller has privileged identity. |
| 45 | `governance.spec:350-364` / `only_initializer_changes_initialized_field` | C | `S3-2` | Normative | Only initialize may change the initialized bit. |
| 46 | `governance.spec:366-381` / `check_initializer` | C | `S5-2` | Normative | Initialization must revert when repeated and set the initialized bit upon success. |
| 47 | `governancePrivileged.spec:18-37` / `privilegedOperation` | C | `S5-3` | Diagnostic / partial | A selected non-exempt governance operation must not succeed from two distinct senders in identical initial storage; this is only a partial access-control detector. — Partial two-caller access-control detector, not proof of authorized identity. |
| 48 | `governance_old_rules.spec:4-55` / `no_double_vote_referendum_vote` | I | `S6-4` | Normative | A second vote must not improperly alter a record or change multiple vote categories. |
| 49 | `governance_old_rules.spec:60-81` / `sum_of_votes_cannot_exceed_total_weight` | I | `S6-4` | Normative | The sum of yes, no and abstain proposal votes must never exceed locked-gold voting weight. |
| 50 | `governance_old_rules.spec:84-111` / `constitution_change_legal` | I | `UNMAPPED` | Diagnostic / partial | The active property ends with assert true, so it cannot detect an illegal constitution change despite its name/comment. — Active property is assert true; abandoned constitution checks are comments. |
| 51 | `lockedGold.spec:27-41` / `totalNonVotingGEAccountNonVoting` | C | `S6-4` | Normative | The total nonvoting locked-gold balance must not be smaller than any one account's nonvoting balance. |
| 52 | `lockedGold.spec:46-75` / `totalPreserved` | C | `S6-4` | Normative | For a self-initiated operation, the sum of available balance, nonvoting locked gold and pending withdrawals is conserved, subject to explicit selector and queue-length restrictions. |
| 53 | `lockedGold.spec:80-107` / `noChangeByOther` | C | `S3-2` | Normative | A transaction made by a different account must not change another account's nonvoting balance or pending withdrawals; the source handles withdraw differently. |
| 54 | `lockedGold.spec:112-123` / `withdraw` | C | `S6-4` | Diagnostic / partial | Withdrawing a pending amount must increase the receiver's balance by that entry's value; the rule is also a prover-model diagnostic. — Explicitly a prover-model test; ercBalanceOf in harness reads native balance. |
| 55 | `lockedGold.spec:128-150` / `noWithdrawBeforeUnlocking` | C | `S5-2` | Normative | Before the unlocking period has elapsed, newly unlocked funds must remain in the account's locked or pending balances. — Unlock timing via locked-plus-pending bound; not direct withdraw revert. |
| 56 | `lockedGold.spec:155-169` / `only_initializer_changes_initialized_field` | C | `S3-2` | Normative | Only initialize is permitted to change the initialized field. |
| 57 | `lockedGold.spec:176-194` / `check_initializer` | C | `S5-2` | Normative | Initialize must revert if already initialized, or mark initialized if successful. |
| 58 | `locked_gold_linked.spec:4-19` / `no_validate_delegation_when_validating` | I | `S5-2` | Normative | A caller already validating must not succeed in delegating validation. |
| 59 | `locked_gold_linked.spec:24-39` / `no_vote_delegation_when_voting` | I | `S5-2` | Normative | A caller already voting must not successfully delegate voting. |
| 60 | `locked_gold_linked.spec:44-61` / `no_weight_changing_when_voting` | I | `S3-2` | Normative | A currently voting account's weight must not be changed by the selected operation. |
| 61 | `reserve.spec:10-29` / `nonspenderCantReduceBalance` | I | `S5-1` | Normative | An address that is neither spender nor exchange must not decrease the reserve's balance through a fallback call, nor change it at all through other calls. |

## Validation evidence and unresolved quality work

**Independent connector-based structural audit on the branch:** after reading the full CSV as RFC-4180 (quoted fields, commas and CRLF), the branch tree was checked for all referenced example paths, `complete`/ `incomplete` file-shapes, permitted labels, allowed result/outcome values, a single Project 9 contest entry, numeric IDs, orphan artifacts and the seven report findings. Result: **61 valid rows, 61 unique examples, 52 complete, 9 incomplete, 4 UNMAPPED, 192 referenced artifacts, 7 report issues, 0 detected structural inconsistencies**. This is **not** a substitute for the project's Python validators.

**Subsequent source-literal audit:** all **61 of 61** extracted property bodies were compared byte-for-byte as textual spans against their original `.spec` file/line interval; no altered or missing assertions, filters, or `preserved` blocks were detected. Separately, all 61 CSV Property values and start lines were checked against live source declarations, with **0 mismatches**. Comparing the branch tree to its main-branch base identified exactly **393 changed paths**: 195 snapshot source files, 192 example artifacts, the PDF, the report index, this document and 3 shared CSVs; **0 paths outside the allowed Project 9 scope** and **0 deleted files**. These are executed connector-assisted integrity checks, not proof of CVL compilation.

**Requested exact commands, not yet executed in an eligible repository shell:**

```sh
cd Web3Bugs-certora
python scripts/check_specs.py .
python scripts/check_contests_csv.py .
python scripts/check_contracts.py .
git diff --check
```

The connected Desktop Commander machine is offline, and the local execution container cannot resolve github.com or raw.githubusercontent.com; it cannot clone/check the full remote branch. Therefore the **three Python checks and `git diff --check` have no genuine PASS/FAIL logs yet** and must be run by the independent reviewer or CI. The source snapshot contains legacy trailing whitespace and historical line endings; do not normalize them merely to make diff checks quiet.

**Other open review items:** complete a full faithful Markdown transcription of the original 14-page PDF (only an indexed report Markdown is present, with byte-identical authoritative PDF); independently spot-check each `.sol` excerpt and CVL method signature against compiled historical target ABI; obtain missing configurations/harnesses for the nine incomplete examples; and run native scripts in a checked-out repository. This PR must remain **Draft** until such work is resolved or explicitly accepted by the orchestrator.

## Catalog locations

- Indexed relationships: `results/spec/spec_buglabel.csv`.
- Complete and incomplete Project 9 examples: `results/spec/complete/9/` and `results/spec/incomplete/9/`.
- Original immutable snapshot: `contracts/9/`; preserved PDF: `resources/9/CeloMay2020.pdf`; topical report index: `reports/9.md`.
- Contest metadata and original findings: `results/contests.csv`, `results/bugs.csv`.
