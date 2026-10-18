// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: GovernorPreventLateQuorum.spec:87-95 quorumReachedEffect

// Original: contracts/18/contracts/governance/Governor.sol lines 203-203 function/modifier _quorumReached
    function _quorumReached(uint256 proposalId) internal view virtual returns (bool);

// Original: contracts/18/contracts/governance/extensions/GovernorCountingSimple.sol lines 67-71 function/modifier _quorumReached
    function _quorumReached(uint256 proposalId) internal view virtual override returns (bool) {
        ProposalVote storage proposalvote = _proposalVotes[proposalId];

        return quorum(proposalSnapshot(proposalId)) <= proposalvote.forVotes + proposalvote.abstainVotes;
    }

// Original: contracts/18/contracts/governance/Governor.sol lines 47-47 state declaration
    mapping(uint256 => ProposalCore) private _proposals;

// Original: contracts/18/contracts/governance/extensions/GovernorCountingSimple.sol lines 30-30 state declaration
    mapping(uint256 => ProposalVote) private _proposalVotes;

// Original: contracts/18/contracts/governance/extensions/GovernorVotesQuorumFraction.sol lines 15-15 state declaration
    uint256 private _quorumNumerator;
