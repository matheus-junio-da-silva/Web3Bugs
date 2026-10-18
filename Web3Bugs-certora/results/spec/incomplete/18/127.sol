// Historical Solidity excerpts; not a compilable harness.
// Original: contracts/18/contracts/governance/extensions/GovernorPreventLateQuorum.sol lines 46-69 (callable)
    function proposalDeadline(uint256 proposalId) public view virtual override returns (uint256) {
        return Math.max(super.proposalDeadline(proposalId), _extendedDeadlines[proposalId].getDeadline());
    }

    /**
     * @dev Casts a vote and detects if it caused quorum to be reached, potentially extending the voting period. See
     * {Governor-_castVote}.
     *
     * May emit a {ProposalExtended} event.
     */
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

// Original: contracts/18/contracts/governance/Governor.sol lines 189-212 (callable)
    function proposalDeadline(uint256 proposalId) public view virtual override returns (uint256) {
        return _proposals[proposalId].voteEnd.getDeadline();
    }

    /**
     * @dev Part of the Governor Bravo's interface: _"The number of votes required in order for a voter to become a proposer"_.
     */
    function proposalThreshold() public view virtual returns (uint256) {
        return 0;
    }

    /**
     * @dev Amount of votes already cast passes the threshold limit.
     */
    function _quorumReached(uint256 proposalId) internal view virtual returns (bool);

    /**
     * @dev Is the proposal successful or not.
     */
    function _voteSucceeded(uint256 proposalId) internal view virtual returns (bool);

    /**
     * @dev Get the voting weight of `account` at a specific `blockNumber`, for a vote as described by `params`.
     */

// Original: contracts/18/contracts/mocks/GovernorPreventLateQuorumMock.sol lines 34-57 (callable)
    function quorum(uint256) public view virtual override returns (uint256) {
        return _quorum;
    }

    function proposalDeadline(uint256 proposalId)
        public
        view
        virtual
        override(Governor, GovernorPreventLateQuorum)
        returns (uint256)
    {
        return super.proposalDeadline(proposalId);
    }

    function proposalThreshold() public view virtual override(Governor, GovernorSettings) returns (uint256) {
        return super.proposalThreshold();
    }

    function _castVote(
        uint256 proposalId,
        address account,
        uint8 support,
        string memory reason,
        bytes memory params

// Original: contracts/18/contracts/mocks/GovernorPreventLateQuorumMock.sol lines 38-61 (callable)
    function proposalDeadline(uint256 proposalId)
        public
        view
        virtual
        override(Governor, GovernorPreventLateQuorum)
        returns (uint256)
    {
        return super.proposalDeadline(proposalId);
    }

    function proposalThreshold() public view virtual override(Governor, GovernorSettings) returns (uint256) {
        return super.proposalThreshold();
    }

    function _castVote(
        uint256 proposalId,
        address account,
        uint8 support,
        string memory reason,
        bytes memory params
    ) internal virtual override(Governor, GovernorPreventLateQuorum) returns (uint256) {
        return super._castVote(proposalId, account, support, reason, params);
    }
}
