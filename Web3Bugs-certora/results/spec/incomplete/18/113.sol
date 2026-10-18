// Historical Solidity excerpts; not a compilable harness.
// Original: contracts/18/contracts/governance/Governor.sol lines 289-312 (callable)
    function execute(
        address[] memory targets,
        uint256[] memory values,
        bytes[] memory calldatas,
        bytes32 descriptionHash
    ) public payable virtual override returns (uint256) {
        uint256 proposalId = hashProposal(targets, values, calldatas, descriptionHash);

        ProposalState status = state(proposalId);
        require(
            status == ProposalState.Succeeded || status == ProposalState.Queued,
            "Governor: proposal not successful"
        );
        _proposals[proposalId].executed = true;

        emit ProposalExecuted(proposalId);

        _beforeExecute(proposalId, targets, values, calldatas, descriptionHash);
        _execute(proposalId, targets, values, calldatas, descriptionHash);
        _afterExecute(proposalId, targets, values, calldatas, descriptionHash);

        return proposalId;
    }

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
