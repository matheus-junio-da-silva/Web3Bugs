// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: RulesInProgress.spec:116-139 possibleTotalVotes

// Original: contracts/18/contracts/governance/Governor.sol lines 182-184 function/modifier proposalSnapshot
    function proposalSnapshot(uint256 proposalId) public view virtual override returns (uint256) {
        return _proposals[proposalId].voteStart.getDeadline();
    }

// Original: contracts/18/contracts/governance/Governor.sol lines 413-416 function/modifier castVote
    function castVote(uint256 proposalId, uint8 support) public virtual override returns (uint256) {
        address voter = _msgSender();
        return _castVote(proposalId, voter, support, "");
    }

// Original: contracts/18/contracts/governance/extensions/GovernorCountingSimple.sol lines 50-62 function/modifier proposalVotes
    function proposalVotes(uint256 proposalId)
        public
        view
        virtual
        returns (
            uint256 againstVotes,
            uint256 forVotes,
            uint256 abstainVotes
        )
    {
        ProposalVote storage proposalvote = _proposalVotes[proposalId];
        return (proposalvote.againstVotes, proposalvote.forVotes, proposalvote.abstainVotes);
    }

// Original: contracts/18/contracts/governance/extensions/GovernorCountingSimple.sol lines 30-30 state declaration
    mapping(uint256 => ProposalVote) private _proposalVotes;
