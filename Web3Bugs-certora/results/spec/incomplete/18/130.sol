// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: GovernorPreventLateQuorum.spec:242-257 deadlineExtenededIfQuorumReached

// Original: contracts/18/contracts/governance/extensions/GovernorPreventLateQuorum.sol lines 46-48 function/modifier proposalDeadline
    function proposalDeadline(uint256 proposalId) public view virtual override returns (uint256) {
        return Math.max(super.proposalDeadline(proposalId), _extendedDeadlines[proposalId].getDeadline());
    }

// Original: contracts/18/contracts/governance/extensions/GovernorPreventLateQuorum.sol lines 84-86 function/modifier lateQuorumVoteExtension
    function lateQuorumVoteExtension() public view virtual returns (uint64) {
        return _voteExtension;
    }

// Original: contracts/18/contracts/governance/Governor.sol lines 189-191 function/modifier proposalDeadline
    function proposalDeadline(uint256 proposalId) public view virtual override returns (uint256) {
        return _proposals[proposalId].voteEnd.getDeadline();
    }

// Original: contracts/18/contracts/mocks/GovernorPreventLateQuorumMock.sol lines 38-46 function/modifier proposalDeadline
    function proposalDeadline(uint256 proposalId)
        public
        view
        virtual
        override(Governor, GovernorPreventLateQuorum)
        returns (uint256)
    {
        return super.proposalDeadline(proposalId);
    }

// Original: contracts/18/contracts/governance/extensions/GovernorPreventLateQuorum.sol lines 25-25 state declaration
    mapping(uint256 => Timers.BlockNumber) private _extendedDeadlines;

// Original: contracts/18/contracts/governance/Governor.sol lines 47-47 state declaration
    mapping(uint256 => ProposalCore) private _proposals;

// Original: contracts/18/contracts/governance/extensions/GovernorCountingSimple.sol lines 30-30 state declaration
    mapping(uint256 => ProposalVote) private _proposalVotes;

// Original: contracts/18/contracts/governance/extensions/GovernorVotesQuorumFraction.sol lines 15-15 state declaration
    uint256 private _quorumNumerator;
