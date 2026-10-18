// Historical Solidity excerpts; not a compilable harness.
// Original: contracts/18/contracts/governance/Governor.sol lines 182-205 (callable)
    function proposalSnapshot(uint256 proposalId) public view virtual override returns (uint256) {
        return _proposals[proposalId].voteStart.getDeadline();
    }

    /**
     * @dev See {IGovernor-proposalDeadline}.
     */
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

// Original: contracts/18/contracts/mocks/GovernorMock.sol lines 9-24 (target context (no matched entrypoint))

contract GovernorMock is
    GovernorProposalThreshold,
    GovernorSettings,
    GovernorVotesQuorumFraction,
    GovernorCountingSimple
{
    constructor(
        string memory name_,
        IVotes token_,
        uint256 votingDelay_,
        uint256 votingPeriod_,
        uint256 quorumNumerator_
    )
        Governor(name_)
        GovernorSettings(votingDelay_, votingPeriod_, 0)
