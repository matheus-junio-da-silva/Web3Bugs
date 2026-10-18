// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: GovernorBase.spec:331-341 executedOnlyAfterExecuteFunc

// Original: contracts/18/contracts/governance/Governor.sol lines 289-311 function/modifier execute
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

// Original: contracts/18/contracts/governance/Governor.sol lines 47-47 state declaration
    mapping(uint256 => ProposalCore) private _proposals;
