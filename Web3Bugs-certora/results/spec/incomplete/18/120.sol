// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: GovernorCountingSimple.spec:194-205 privilegedOnlyNumerator

// Original: contracts/18/contracts/governance/extensions/GovernorVotesQuorumFraction.sol lines 33-35 function/modifier quorumNumerator
    function quorumNumerator() public view virtual returns (uint256) {
        return _quorumNumerator;
    }

// Original: contracts/18/contracts/governance/extensions/GovernorVotesQuorumFraction.sol lines 15-15 state declaration
    uint256 private _quorumNumerator;
