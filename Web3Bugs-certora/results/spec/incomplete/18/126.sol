// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: GovernorPreventLateQuorum.spec:141-154 deadlineCantBeUnextended

// Original: contracts/18/contracts/governance/extensions/GovernorPreventLateQuorum.sol lines 25-25 state declaration
    mapping(uint256 => Timers.BlockNumber) private _extendedDeadlines;

// Original: contracts/18/contracts/governance/Governor.sol lines 47-47 state declaration
    mapping(uint256 => ProposalCore) private _proposals;
