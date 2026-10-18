// Historical Solidity excerpts; not a compilable harness.
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
