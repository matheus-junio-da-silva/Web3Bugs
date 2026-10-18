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

// Original: contracts/18/contracts/governance/Governor.sol lines 20-35 (target context (no matched entrypoint))
 *
 * This contract is abstract and requires several function to be implemented in various modules:
 *
 * - A counting module must implement {quorum}, {_quorumReached}, {_voteSucceeded} and {_countVote}
 * - A voting module must implement {_getVotes}
 * - Additionanly, the {votingPeriod} must also be implemented
 *
 * _Available since v4.3._
 */
abstract contract Governor is Context, ERC165, EIP712, IGovernor, IERC721Receiver, IERC1155Receiver {
    using DoubleEndedQueue for DoubleEndedQueue.Bytes32Deque;
    using SafeCast for uint256;
    using Timers for Timers.BlockNumber;

    bytes32 public constant BALLOT_TYPEHASH = keccak256("Ballot(uint256 proposalId,uint8 support)");
    bytes32 public constant EXTENDED_BALLOT_TYPEHASH =

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
