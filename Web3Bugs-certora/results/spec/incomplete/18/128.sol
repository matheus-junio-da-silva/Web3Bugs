// Historical Solidity excerpts; not a compilable harness.
// Original: contracts/18/contracts/governance/extensions/GovernorPreventLateQuorum.sol lines 19-34 (target context (no matched entrypoint))
 */
abstract contract GovernorPreventLateQuorum is Governor {
    using SafeCast for uint256;
    using Timers for Timers.BlockNumber;

    uint64 private _voteExtension;
    mapping(uint256 => Timers.BlockNumber) private _extendedDeadlines;

    /// @dev Emitted when a proposal deadline is pushed back due to reaching quorum late in its voting period.
    event ProposalExtended(uint256 indexed proposalId, uint64 extendedDeadline);

    /// @dev Emitted when the {lateQuorumVoteExtension} parameter is changed.
    event LateQuorumVoteExtensionSet(uint64 oldVoteExtension, uint64 newVoteExtension);

    /**
     * @dev Initializes the vote extension parameter: the number of blocks that are required to pass since a proposal

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

// Original: contracts/18/contracts/governance/Governor.sol lines 395-418 (callable)
    function getVotes(address account, uint256 blockNumber) public view virtual override returns (uint256) {
        return _getVotes(account, blockNumber, _defaultParams());
    }

    /**
     * @dev See {IGovernor-getVotesWithParams}.
     */
    function getVotesWithParams(
        address account,
        uint256 blockNumber,
        bytes memory params
    ) public view virtual override returns (uint256) {
        return _getVotes(account, blockNumber, params);
    }

    /**
     * @dev See {IGovernor-castVote}.
     */
    function castVote(uint256 proposalId, uint8 support) public virtual override returns (uint256) {
        address voter = _msgSender();
        return _castVote(proposalId, voter, support, "");
    }

    /**

// Original: contracts/18/contracts/mocks/GovernorPreventLateQuorumMock.sol lines 9-24 (target context (no matched entrypoint))

contract GovernorPreventLateQuorumMock is
    GovernorSettings,
    GovernorVotes,
    GovernorCountingSimple,
    GovernorPreventLateQuorum
{
    uint256 private _quorum;

    constructor(
        string memory name_,
        IVotes token_,
        uint256 votingDelay_,
        uint256 votingPeriod_,
        uint256 quorum_,
        uint64 voteExtension_
