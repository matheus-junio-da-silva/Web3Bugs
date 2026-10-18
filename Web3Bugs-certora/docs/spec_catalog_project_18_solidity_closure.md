# Project 18 — Historical Solidity import/inheritance closure

Source integrity: all 307 original text/source files match the PropertyGPT historical snapshot byte-for-byte. Original PDF SHA-256: 4a35df36c47e6e7e2b4333cb3890bc2a8cbca569e32b2fc6f24820b8a56cbc37.

This is a graph of local Solidity imports in the retained source, NOT a reconstruction of the historical runtime harness or munged ABI. Existing imports do not guarantee formal reproducibility.

| Spec | Target context | Candidate files | Import closure (files) | Missing local imports |
| --- | --- | ---: | ---: | ---: |
| AccessControl.spec | AccessControlMock | 2 | 7 | 0 |
| ERC1155.spec | ERC1155Mock | 2 | 9 | 0 |
| ERC1155Burnable.spec | ERC1155BurnableMock | 3 | 10 | 0 |
| ERC1155Pausable.spec | ERC1155PausableMock | 3 | 12 | 0 |
| ERC1155Supply.spec | ERC1155Supply (historical verification harness) | 2 | 11 | 0 |
| ERC20FlashMint.spec | ERC20FlashMintMock | 2 | 8 | 0 |
| ERC20Votes.spec | ERC20Votes (historical voting harness) | 3 | 17 | 0 |
| ERC20Wrapper.spec | ERC20Wrapper (historical underlying-token harness) | 2 | 9 | 0 |
| ERC721Votes.spec | ERC721Votes (historical voting harness) | 1 | 19 | 0 |
| GovernorBase.spec | Governor (historical ERC20VotesHarness) | 2 | 21 | 0 |
| GovernorCountingSimple.spec | GovernorCountingSimple (historical governor harness) | 2 | 15 | 0 |
| GovernorPreventLateQuorum.spec | GovernorPreventLateQuorumHarness | 3 | 21 | 0 |
| Initializable.spec | Initializable (historical two harness configurations) | 4 | 5 | 0 |
| RulesInProgress.spec | Governor (RulesInProgress; historical ERC20VotesHarness) | 2 | 15 | 0 |
| TimelockController.spec | TimelockController | 1 | 10 | 0 |
| sanity.spec | UNRESOLVED (generic method probe) | 1 | 14 | 0 |

## Exact dependency inventory by source

### AccessControl.spec

Target: AccessControlMock

Source entry files: contracts/18/contracts/access/AccessControl.sol; contracts/18/contracts/mocks/AccessControlMock.sol.

Resolved transitive Solidity sources: contracts/18/contracts/access/AccessControl.sol; contracts/18/contracts/access/IAccessControl.sol; contracts/18/contracts/mocks/AccessControlMock.sol; contracts/18/contracts/utils/Context.sol; contracts/18/contracts/utils/Strings.sol; contracts/18/contracts/utils/introspection/ERC165.sol; contracts/18/contracts/utils/introspection/IERC165.sol.

Absent imports: [].

### ERC1155.spec

Target: ERC1155Mock

Source entry files: contracts/18/contracts/token/ERC1155/ERC1155.sol; contracts/18/contracts/mocks/ERC1155Mock.sol.

Resolved transitive Solidity sources: contracts/18/contracts/mocks/ERC1155Mock.sol; contracts/18/contracts/token/ERC1155/ERC1155.sol; contracts/18/contracts/token/ERC1155/IERC1155.sol; contracts/18/contracts/token/ERC1155/IERC1155Receiver.sol; contracts/18/contracts/token/ERC1155/extensions/IERC1155MetadataURI.sol; contracts/18/contracts/utils/Address.sol; contracts/18/contracts/utils/Context.sol; contracts/18/contracts/utils/introspection/ERC165.sol; contracts/18/contracts/utils/introspection/IERC165.sol.

Absent imports: [].

### ERC1155Burnable.spec

Target: ERC1155BurnableMock

Source entry files: contracts/18/contracts/token/ERC1155/extensions/ERC1155Burnable.sol; contracts/18/contracts/mocks/ERC1155BurnableMock.sol; contracts/18/contracts/token/ERC1155/ERC1155.sol.

Resolved transitive Solidity sources: contracts/18/contracts/mocks/ERC1155BurnableMock.sol; contracts/18/contracts/token/ERC1155/ERC1155.sol; contracts/18/contracts/token/ERC1155/IERC1155.sol; contracts/18/contracts/token/ERC1155/IERC1155Receiver.sol; contracts/18/contracts/token/ERC1155/extensions/ERC1155Burnable.sol; contracts/18/contracts/token/ERC1155/extensions/IERC1155MetadataURI.sol; contracts/18/contracts/utils/Address.sol; contracts/18/contracts/utils/Context.sol; contracts/18/contracts/utils/introspection/ERC165.sol; contracts/18/contracts/utils/introspection/IERC165.sol.

Absent imports: [].

### ERC1155Pausable.spec

Target: ERC1155PausableMock

Source entry files: contracts/18/contracts/token/ERC1155/extensions/ERC1155Pausable.sol; contracts/18/contracts/mocks/ERC1155PausableMock.sol; contracts/18/contracts/token/ERC1155/ERC1155.sol.

Resolved transitive Solidity sources: contracts/18/contracts/mocks/ERC1155Mock.sol; contracts/18/contracts/mocks/ERC1155PausableMock.sol; contracts/18/contracts/security/Pausable.sol; contracts/18/contracts/token/ERC1155/ERC1155.sol; contracts/18/contracts/token/ERC1155/IERC1155.sol; contracts/18/contracts/token/ERC1155/IERC1155Receiver.sol; contracts/18/contracts/token/ERC1155/extensions/ERC1155Pausable.sol; contracts/18/contracts/token/ERC1155/extensions/IERC1155MetadataURI.sol; contracts/18/contracts/utils/Address.sol; contracts/18/contracts/utils/Context.sol; contracts/18/contracts/utils/introspection/ERC165.sol; contracts/18/contracts/utils/introspection/IERC165.sol.

Absent imports: [].

### ERC1155Supply.spec

Target: ERC1155Supply (historical verification harness)

Source entry files: contracts/18/contracts/token/ERC1155/extensions/ERC1155Supply.sol; contracts/18/contracts/mocks/ERC1155SupplyMock.sol.

Resolved transitive Solidity sources: contracts/18/contracts/mocks/ERC1155Mock.sol; contracts/18/contracts/mocks/ERC1155SupplyMock.sol; contracts/18/contracts/token/ERC1155/ERC1155.sol; contracts/18/contracts/token/ERC1155/IERC1155.sol; contracts/18/contracts/token/ERC1155/IERC1155Receiver.sol; contracts/18/contracts/token/ERC1155/extensions/ERC1155Supply.sol; contracts/18/contracts/token/ERC1155/extensions/IERC1155MetadataURI.sol; contracts/18/contracts/utils/Address.sol; contracts/18/contracts/utils/Context.sol; contracts/18/contracts/utils/introspection/ERC165.sol; contracts/18/contracts/utils/introspection/IERC165.sol.

Absent imports: [].

### ERC20FlashMint.spec

Target: ERC20FlashMintMock

Source entry files: contracts/18/contracts/token/ERC20/extensions/ERC20FlashMint.sol; contracts/18/contracts/mocks/ERC20FlashMintMock.sol.

Resolved transitive Solidity sources: contracts/18/contracts/interfaces/IERC3156FlashBorrower.sol; contracts/18/contracts/interfaces/IERC3156FlashLender.sol; contracts/18/contracts/mocks/ERC20FlashMintMock.sol; contracts/18/contracts/token/ERC20/ERC20.sol; contracts/18/contracts/token/ERC20/IERC20.sol; contracts/18/contracts/token/ERC20/extensions/ERC20FlashMint.sol; contracts/18/contracts/token/ERC20/extensions/IERC20Metadata.sol; contracts/18/contracts/utils/Context.sol.

Absent imports: [].

### ERC20Votes.spec

Target: ERC20Votes (historical voting harness)

Source entry files: contracts/18/contracts/token/ERC20/extensions/ERC20Votes.sol; contracts/18/contracts/mocks/ERC20VotesMock.sol; contracts/18/contracts/governance/utils/Votes.sol.

Resolved transitive Solidity sources: contracts/18/contracts/governance/utils/IVotes.sol; contracts/18/contracts/governance/utils/Votes.sol; contracts/18/contracts/mocks/ERC20VotesMock.sol; contracts/18/contracts/token/ERC20/ERC20.sol; contracts/18/contracts/token/ERC20/IERC20.sol; contracts/18/contracts/token/ERC20/extensions/ERC20Votes.sol; contracts/18/contracts/token/ERC20/extensions/IERC20Metadata.sol; contracts/18/contracts/token/ERC20/extensions/draft-ERC20Permit.sol; contracts/18/contracts/token/ERC20/extensions/draft-IERC20Permit.sol; contracts/18/contracts/utils/Checkpoints.sol; contracts/18/contracts/utils/Context.sol; contracts/18/contracts/utils/Counters.sol; contracts/18/contracts/utils/Strings.sol; contracts/18/contracts/utils/cryptography/ECDSA.sol; contracts/18/contracts/utils/cryptography/draft-EIP712.sol; contracts/18/contracts/utils/math/Math.sol; contracts/18/contracts/utils/math/SafeCast.sol.

Absent imports: [].

### ERC20Wrapper.spec

Target: ERC20Wrapper (historical underlying-token harness)

Source entry files: contracts/18/contracts/token/ERC20/extensions/ERC20Wrapper.sol; contracts/18/contracts/mocks/ERC20WrapperMock.sol.

Resolved transitive Solidity sources: contracts/18/contracts/mocks/ERC20WrapperMock.sol; contracts/18/contracts/token/ERC20/ERC20.sol; contracts/18/contracts/token/ERC20/IERC20.sol; contracts/18/contracts/token/ERC20/extensions/ERC20Wrapper.sol; contracts/18/contracts/token/ERC20/extensions/IERC20Metadata.sol; contracts/18/contracts/token/ERC20/extensions/draft-IERC20Permit.sol; contracts/18/contracts/token/ERC20/utils/SafeERC20.sol; contracts/18/contracts/utils/Address.sol; contracts/18/contracts/utils/Context.sol.

Absent imports: [].

### ERC721Votes.spec

Target: ERC721Votes (historical voting harness)

Source entry files: contracts/18/contracts/mocks/ERC721VotesMock.sol.

Resolved transitive Solidity sources: contracts/18/contracts/governance/utils/IVotes.sol; contracts/18/contracts/governance/utils/Votes.sol; contracts/18/contracts/mocks/ERC721VotesMock.sol; contracts/18/contracts/token/ERC721/ERC721.sol; contracts/18/contracts/token/ERC721/IERC721.sol; contracts/18/contracts/token/ERC721/IERC721Receiver.sol; contracts/18/contracts/token/ERC721/extensions/IERC721Metadata.sol; contracts/18/contracts/token/ERC721/extensions/draft-ERC721Votes.sol; contracts/18/contracts/utils/Address.sol; contracts/18/contracts/utils/Checkpoints.sol; contracts/18/contracts/utils/Context.sol; contracts/18/contracts/utils/Counters.sol; contracts/18/contracts/utils/Strings.sol; contracts/18/contracts/utils/cryptography/ECDSA.sol; contracts/18/contracts/utils/cryptography/draft-EIP712.sol; contracts/18/contracts/utils/introspection/ERC165.sol; contracts/18/contracts/utils/introspection/IERC165.sol; contracts/18/contracts/utils/math/Math.sol; contracts/18/contracts/utils/math/SafeCast.sol.

Absent imports: [].

### GovernorBase.spec

Target: Governor (historical ERC20VotesHarness)

Source entry files: contracts/18/contracts/governance/Governor.sol; contracts/18/contracts/mocks/GovernorMock.sol.

Resolved transitive Solidity sources: contracts/18/contracts/governance/Governor.sol; contracts/18/contracts/governance/IGovernor.sol; contracts/18/contracts/governance/extensions/GovernorCountingSimple.sol; contracts/18/contracts/governance/extensions/GovernorProposalThreshold.sol; contracts/18/contracts/governance/extensions/GovernorSettings.sol; contracts/18/contracts/governance/extensions/GovernorVotes.sol; contracts/18/contracts/governance/extensions/GovernorVotesQuorumFraction.sol; contracts/18/contracts/governance/utils/IVotes.sol; contracts/18/contracts/mocks/GovernorMock.sol; contracts/18/contracts/token/ERC1155/IERC1155Receiver.sol; contracts/18/contracts/token/ERC721/IERC721Receiver.sol; contracts/18/contracts/utils/Address.sol; contracts/18/contracts/utils/Context.sol; contracts/18/contracts/utils/Strings.sol; contracts/18/contracts/utils/Timers.sol; contracts/18/contracts/utils/cryptography/ECDSA.sol; contracts/18/contracts/utils/cryptography/draft-EIP712.sol; contracts/18/contracts/utils/introspection/ERC165.sol; contracts/18/contracts/utils/introspection/IERC165.sol; contracts/18/contracts/utils/math/SafeCast.sol; contracts/18/contracts/utils/structs/DoubleEndedQueue.sol.

Absent imports: [].

### GovernorCountingSimple.spec

Target: GovernorCountingSimple (historical governor harness)

Source entry files: contracts/18/contracts/governance/extensions/GovernorCountingSimple.sol; contracts/18/contracts/governance/Governor.sol.

Resolved transitive Solidity sources: contracts/18/contracts/governance/Governor.sol; contracts/18/contracts/governance/IGovernor.sol; contracts/18/contracts/governance/extensions/GovernorCountingSimple.sol; contracts/18/contracts/token/ERC1155/IERC1155Receiver.sol; contracts/18/contracts/token/ERC721/IERC721Receiver.sol; contracts/18/contracts/utils/Address.sol; contracts/18/contracts/utils/Context.sol; contracts/18/contracts/utils/Strings.sol; contracts/18/contracts/utils/Timers.sol; contracts/18/contracts/utils/cryptography/ECDSA.sol; contracts/18/contracts/utils/cryptography/draft-EIP712.sol; contracts/18/contracts/utils/introspection/ERC165.sol; contracts/18/contracts/utils/introspection/IERC165.sol; contracts/18/contracts/utils/math/SafeCast.sol; contracts/18/contracts/utils/structs/DoubleEndedQueue.sol.

Absent imports: [].

### GovernorPreventLateQuorum.spec

Target: GovernorPreventLateQuorumHarness

Source entry files: contracts/18/contracts/governance/extensions/GovernorPreventLateQuorum.sol; contracts/18/contracts/governance/Governor.sol; contracts/18/contracts/mocks/GovernorPreventLateQuorumMock.sol.

Resolved transitive Solidity sources: contracts/18/contracts/governance/Governor.sol; contracts/18/contracts/governance/IGovernor.sol; contracts/18/contracts/governance/extensions/GovernorCountingSimple.sol; contracts/18/contracts/governance/extensions/GovernorPreventLateQuorum.sol; contracts/18/contracts/governance/extensions/GovernorSettings.sol; contracts/18/contracts/governance/extensions/GovernorVotes.sol; contracts/18/contracts/governance/utils/IVotes.sol; contracts/18/contracts/mocks/GovernorPreventLateQuorumMock.sol; contracts/18/contracts/token/ERC1155/IERC1155Receiver.sol; contracts/18/contracts/token/ERC721/IERC721Receiver.sol; contracts/18/contracts/utils/Address.sol; contracts/18/contracts/utils/Context.sol; contracts/18/contracts/utils/Strings.sol; contracts/18/contracts/utils/Timers.sol; contracts/18/contracts/utils/cryptography/ECDSA.sol; contracts/18/contracts/utils/cryptography/draft-EIP712.sol; contracts/18/contracts/utils/introspection/ERC165.sol; contracts/18/contracts/utils/introspection/IERC165.sol; contracts/18/contracts/utils/math/Math.sol; contracts/18/contracts/utils/math/SafeCast.sol; contracts/18/contracts/utils/structs/DoubleEndedQueue.sol.

Absent imports: [].

### Initializable.spec

Target: Initializable (historical two harness configurations)

Source entry files: contracts/18/contracts/proxy/utils/Initializable.sol; contracts/18/contracts/mocks/InitializableMock.sol; contracts/18/contracts/mocks/MultipleInheritanceInitializableMocks.sol; contracts/18/contracts/mocks/SingleInheritanceInitializableMocks.sol.

Resolved transitive Solidity sources: contracts/18/contracts/mocks/InitializableMock.sol; contracts/18/contracts/mocks/MultipleInheritanceInitializableMocks.sol; contracts/18/contracts/mocks/SingleInheritanceInitializableMocks.sol; contracts/18/contracts/proxy/utils/Initializable.sol; contracts/18/contracts/utils/Address.sol.

Absent imports: [].

### RulesInProgress.spec

Target: Governor (RulesInProgress; historical ERC20VotesHarness)

Source entry files: contracts/18/contracts/governance/Governor.sol; contracts/18/contracts/governance/extensions/GovernorCountingSimple.sol.

Resolved transitive Solidity sources: contracts/18/contracts/governance/Governor.sol; contracts/18/contracts/governance/IGovernor.sol; contracts/18/contracts/governance/extensions/GovernorCountingSimple.sol; contracts/18/contracts/token/ERC1155/IERC1155Receiver.sol; contracts/18/contracts/token/ERC721/IERC721Receiver.sol; contracts/18/contracts/utils/Address.sol; contracts/18/contracts/utils/Context.sol; contracts/18/contracts/utils/Strings.sol; contracts/18/contracts/utils/Timers.sol; contracts/18/contracts/utils/cryptography/ECDSA.sol; contracts/18/contracts/utils/cryptography/draft-EIP712.sol; contracts/18/contracts/utils/introspection/ERC165.sol; contracts/18/contracts/utils/introspection/IERC165.sol; contracts/18/contracts/utils/math/SafeCast.sol; contracts/18/contracts/utils/structs/DoubleEndedQueue.sol.

Absent imports: [].

### TimelockController.spec

Target: TimelockController

Source entry files: contracts/18/contracts/governance/TimelockController.sol.

Resolved transitive Solidity sources: contracts/18/contracts/access/AccessControl.sol; contracts/18/contracts/access/IAccessControl.sol; contracts/18/contracts/governance/TimelockController.sol; contracts/18/contracts/token/ERC1155/IERC1155Receiver.sol; contracts/18/contracts/token/ERC721/IERC721Receiver.sol; contracts/18/contracts/utils/Address.sol; contracts/18/contracts/utils/Context.sol; contracts/18/contracts/utils/Strings.sol; contracts/18/contracts/utils/introspection/ERC165.sol; contracts/18/contracts/utils/introspection/IERC165.sol.

Absent imports: [].

### sanity.spec

Target: UNRESOLVED (generic method probe)

Source entry files: contracts/18/contracts/governance/Governor.sol.

Resolved transitive Solidity sources: contracts/18/contracts/governance/Governor.sol; contracts/18/contracts/governance/IGovernor.sol; contracts/18/contracts/token/ERC1155/IERC1155Receiver.sol; contracts/18/contracts/token/ERC721/IERC721Receiver.sol; contracts/18/contracts/utils/Address.sol; contracts/18/contracts/utils/Context.sol; contracts/18/contracts/utils/Strings.sol; contracts/18/contracts/utils/Timers.sol; contracts/18/contracts/utils/cryptography/ECDSA.sol; contracts/18/contracts/utils/cryptography/draft-EIP712.sol; contracts/18/contracts/utils/introspection/ERC165.sol; contracts/18/contracts/utils/introspection/IERC165.sol; contracts/18/contracts/utils/math/SafeCast.sol; contracts/18/contracts/utils/structs/DoubleEndedQueue.sol.

Absent imports: [].

## Preserved non-source barriers

The report names GovernorPreventLateQuorumHarness, customized voter-token harnesses, and initializable flat/multiple-inheritance verification settings that are not present in this tree. They remain incomplete despite the local import graph.
TimelockController.spec declares schedule(address,uint256,bytes32,bytes32,bytes32,uint256), versus historical Solidity accepting bytes as the third argument at TimelockController.sol lines 214–220; dependent examples are incomplete.
RulesInProgress.spec calls hashIdCorrelation and getTimestamp without importing the spec defining those functions. Both active work-in-progress rules are cataloged without assuming proof.
