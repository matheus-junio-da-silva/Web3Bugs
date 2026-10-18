// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: GovernorCountingSimple.spec:132-146 noVoteForSomeoneElse

// Original: contracts/18/contracts/governance/extensions/GovernorCountingSimple.sol lines 43-45 function/modifier hasVoted
    function hasVoted(uint256 proposalId, address account) public view virtual override returns (bool) {
        return _proposalVotes[proposalId].hasVoted[account];
    }

// Original: contracts/18/contracts/governance/Governor.sol lines 413-416 function/modifier castVote
    function castVote(uint256 proposalId, uint8 support) public virtual override returns (uint256) {
        address voter = _msgSender();
        return _castVote(proposalId, voter, support, "");
    }

// Original: contracts/18/contracts/governance/Governor.sol lines 500-507 function/modifier _castVote
    function _castVote(
        uint256 proposalId,
        address account,
        uint8 support,
        string memory reason
    ) internal virtual returns (uint256) {
        return _castVote(proposalId, account, support, reason, _defaultParams());
    }

// Original: contracts/18/contracts/governance/Governor.sol lines 515-535 function/modifier _castVote
    function _castVote(
        uint256 proposalId,
        address account,
        uint8 support,
        string memory reason,
        bytes memory params
    ) internal virtual returns (uint256) {
        ProposalCore storage proposal = _proposals[proposalId];
        require(state(proposalId) == ProposalState.Active, "Governor: vote not currently active");

        uint256 weight = _getVotes(account, proposal.voteStart.getDeadline(), params);
        _countVote(proposalId, account, support, weight, params);

        if (params.length == 0) {
            emit VoteCast(account, proposalId, support, weight, reason);
        } else {
            emit VoteCastWithParams(account, proposalId, support, weight, reason, params);
        }

        return weight;
    }

// Original: contracts/18/contracts/governance/extensions/GovernorCountingSimple.sol lines 27-27 state declaration
        mapping(address => bool) hasVoted;

// Original: contracts/18/contracts/governance/extensions/GovernorCountingSimple.sol lines 30-30 state declaration
    mapping(uint256 => ProposalVote) private _proposalVotes;
