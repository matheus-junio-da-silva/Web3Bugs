// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: GovernorBase.spec:285-303 allFunctionsRevertIfExecuted

// Original: contracts/18/contracts/governance/Governor.sol lines 543-549 function/modifier relay
    function relay(
        address target,
        uint256 value,
        bytes calldata data
    ) external virtual onlyGovernance {
        Address.functionCallWithValue(target, data, value);
    }

// Original: contracts/18/contracts/governance/Governor.sol lines 47-47 state declaration
    mapping(uint256 => ProposalCore) private _proposals;
