// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: GovernorPreventLateQuorum.spec:123-133 deadlineChangeEffects

// Original: contracts/18/contracts/governance/extensions/GovernorPreventLateQuorum.sol lines 46-48 function/modifier proposalDeadline
    function proposalDeadline(uint256 proposalId) public view virtual override returns (uint256) {
        return Math.max(super.proposalDeadline(proposalId), _extendedDeadlines[proposalId].getDeadline());
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

// Original: contracts/18/contracts/governance/extensions/GovernorPreventLateQuorum.sol lines 56-78 function/modifier _castVote
    function _castVote(
        uint256 proposalId,
        address account,
        uint8 support,
        string memory reason,
        bytes memory params
    ) internal virtual override returns (uint256) {
        uint256 result = super._castVote(proposalId, account, support, reason, params);

        Timers.BlockNumber storage extendedDeadline = _extendedDeadlines[proposalId];

        if (extendedDeadline.isUnset() && _quorumReached(proposalId)) {
            uint64 extendedDeadlineValue = block.number.toUint64() + lateQuorumVoteExtension();

            if (extendedDeadlineValue > proposalDeadline(proposalId)) {
                emit ProposalExtended(proposalId, extendedDeadlineValue);
            }

            extendedDeadline.setDeadline(extendedDeadlineValue);
        }

        return result;
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

// Original: contracts/18/contracts/mocks/GovernorPreventLateQuorumMock.sol lines 52-60 function/modifier _castVote
    function _castVote(
        uint256 proposalId,
        address account,
        uint8 support,
        string memory reason,
        bytes memory params
    ) internal virtual override(Governor, GovernorPreventLateQuorum) returns (uint256) {
        return super._castVote(proposalId, account, support, reason, params);
    }

// Original: contracts/18/contracts/governance/extensions/GovernorPreventLateQuorum.sol lines 25-25 state declaration
    mapping(uint256 => Timers.BlockNumber) private _extendedDeadlines;

// Original: contracts/18/contracts/governance/Governor.sol lines 47-47 state declaration
    mapping(uint256 => ProposalCore) private _proposals;
