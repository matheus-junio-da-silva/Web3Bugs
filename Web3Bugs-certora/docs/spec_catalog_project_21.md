# Project 21 — Lido V2 (ECHO): historical catalog and soundness matrix

## Source and scope
- Original source: PropertyGPT/certora_projects/lido_v2. PropertyGPT main SHA 687f654c679ed45ab127b7949e2a29c8f5e491b9. All 58 non-PDF source files copied byte-for-byte under contracts/21, with no changes to Solidity or original CVL.
- Historical PDF: resources/21/Certora-Lido-V2-Audit-Report-04-23.pdf (40 pages, issued 2023-04-27, SHA256 b8acbf2e980db873706a40ac1abefdbffa6ad3e6f649445f2000e93e905f9c5b). Its 40-page text extraction is reports/21.md; the original PDF governs exact typography/tables.
- Active source: only specs/DSM.spec (SHA256 f166f8b394189b3a2396325e343a17550f53d46c2d22f407e93819fcc75cf57b). Exactly 1 rule (depositBufferEtherRevertCheck, original lines 11-35) and 1 invariant (quorumLeGuardian, lines 37-38). Lines 40-49 contain a COMMENTED rule; lines 51-67 are a function helper, not an active property; commented import directives at lines 1-2 are inactive.
- Scope: Web3Bugs-certora Project ID 21 is separate from the unrelated root-level Web3Bugs contracts/21 contest.
- Artifact status: 2 incomplete, 0 complete, 2 UNMAPPED, 2 NOT_STATED Results, 2 NOT_STATED Detection Outcomes. Each example has numeric .spec/.sol/.md/.txt under results/spec/incomplete/21.

## Property-by-property traceability

| Example | Actual CVL assertion | Target evidence | Complete? | Historical Result | Detection Outcome | Bug Label |
| --- | --- | --- | --- | --- | --- | --- |
| 1 depositBufferEtherRevertCheck | depositBufferedEtherHarness@withrevert must NOT revert for unconstrained arguments | DepositSecurityModuleHarness declared but absent; real DepositSecurityModule has distinct depositBufferedEther ABI | incomplete | NOT_STATED | NOT_STATED | UNMAPPED |
| 2 quorumLeGuardian | getGuardianLength() >= getGuardianQuorum() | Missing harness/getGuardianLength; real DepositSecurityModule intentionally permits quorum above count | incomplete | NOT_STATED | NOT_STATED | UNMAPPED |

## Recursive dependency closure

| Symbol / dependency | Available evidence | Limitation |
| --- | --- | --- |
| DSMH.Signature / DepositSecurityModuleHarness | DSM.spec:3,17-19 references only; real DepositSecurityModule.Signature exists | Harness and owner-qualified signature type absent; not interchangeable by assumption |
| depositBufferedEtherHarness | DSM.spec:26-32 symbolic call; real method is depositBufferedEther(uint256,bytes32,bytes32,uint256,uint256,bytes,Signature[]) | No matching harness ABI/body, signatures supplied differently |
| getGuardianLength | DSM.spec:6 methods declaration only; real getGuardians() returns address[] | No actual method implementation, cannot silently replace getter with array length |
| getGuardianQuorum | real DepositSecurityModule.sol:214-216 | Concrete getter available, but does not close missing harness/contract imports |
| Solidity ECDSA | DepositSecurityModule.sol:7 imports ../common/lib/ECDSA.sol | ../common subtree not part of archival snapshot |
| External Lido, router, deposit contract | interface declarations and some mocks under 0.8.9 | no authenticated deployed implementation or Prover linkage |

The CVL methods block uses envfree annotations, not implementations. No active axiom, require, assume, ghost, hook, imported executable spec, or concrete summarized external method effects exist in DSM.spec. No historically authenticated Prover run options were supplied.

## Soundness matrix

| Example | Potential problem | Evidence and conservative finding |
| --- | --- | --- |
| 1 | Assertion too strong: unconditional nonreversion | Real DepositSecurityModule.sol:419 reverts if quorum=0 or signatures insufficient, plus other guards at 422-455. An unrestricted symbolic call need not succeed. Missing harness blocks formal counterexample attribution. No inconsistent CVL axiom demonstrated. |
| 2 | False proposed global invariant under intended behavior | Owner may call setGuardianQuorum(1) with guardians.length=0. DepositSecurityModule.sol:222-229 explicitly INTENTIONALLY allows exceeding guardian count. Therefore 0>=1 fails, assuming missing getter means array length. This is a source-level witness, not an observed Certora result or contract bug. |

No contradictory quantified or algebraic assumptions (as in AAVE Vault) appear in this spec. A false asserted property is not an inconsistent assumed axiom. A Prover assumption of the invariant in any other run cannot be claimed without original invocation, and should be checked if a historical config appears. The complete source dependency graph has missing packages; 2 incomplete examples are justified by concrete missing symbols, independently of soundness.

## Historic PDF mapping, assumptions and limits

- PDF pp.31-32 lists 18 check-marked Deposit Security Module properties with DIFFERENT names: onlyOwnerCanChangeOwner, onlyOwnerCanChangePauseIntentValidityPeriodBlocks, onlyOwnerCanChangeMaxDepositsPerBlock, onlyOwnerCanChangeMinDepositBlockDistance, onlyOwnerCanChangeQuorum, correctQuorumUpdate, onlyOwnerCanChangeGuardians, onlyOwnerCanChangeUnpause, canUnpause, cantStop, cannotDepositDuringPauseBool, cannotDepositDuringPauseRevert, unique, zeroIsNotGuardian, youShallNotPassTwice, nonGuardianCantSign, agreedRevertsSimple, onlyGuardianCanPause.
- The checkmark on correctQuorumUpdate reports an update operation; it does NOT prove a global quorum upper bound. agreedRevertsSimple is a conditional revert property, opposite to the unconditional non-revert rule in DSM.spec.
- Report DSM assumptions (PDF p.31): simplifying _makeBeaconChainDeposits32ETH as an ETH transfer, guardian-array upper bound max_uint128-1, and loop unrolling bounded at 3. There is no script/harness establishing application of those assumptions to the two preserved CVL properties.
- General verification assumptions (PDF p.21) omitted separate MemUtils.sol and SigningKeys.sol for tool compatibility. Such omissions limit historical equivalence.
- The PDF p.19 DSM-related finding L-02 (canDeposit returned true for an unregistered module) is said fixed at commit b944985. The current archived DepositSecurityModule.canDeposit checks hasStakingModule at line 381, so do not confuse post-fix archived code with the finding snapshot.
- The broader findings H-01 frontrun DoS and L-05 nonce-change frontrun are NOT tied by any rule-specific evidence to these two properties.

## Classification and provenance policy
UNMAPPED is a catalog sentinel, not a real bug taxonomy category. It is technically safer than calling the intentional owner quorum configuration an erroneous state update or reporting a legitimate deposit revert as a vulnerability. The PDF does not name either active rule. Therefore Result and Detection Outcome stay NOT_STATED (not VERIFIED, VIOLATED, FINDING, ACCEPTED_BEHAVIOR or NO_FINDING). There was no recovered historical harness/target revision; these examples are historical documentation, not replayable CVL2 specifications. No Certora verification/satisfiability run has been claimed.

## Git whitespace compatibility
The additional contracts/21/.gitattributes metadata overrides trailing-space checking solely on the original DSM.spec, whose lines 48 and 61 contain preserved trailing blanks. Original CVL bytes are unchanged. Generated .sol excerpts were normalized to a single ending newline without changing any Solidity source tokens. The repository-wide mandated git diff --check command remains effective for all other added content.
