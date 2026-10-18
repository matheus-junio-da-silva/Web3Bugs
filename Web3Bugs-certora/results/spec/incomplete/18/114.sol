// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: GovernorCountingSimple.spec:100-106 SumOfVotesCastEqualSumOfPowerOfVotedPerProposal

// Original: contracts/18/contracts/governance/extensions/GovernorCountingSimple.sol lines 30-30 state declaration
    mapping(uint256 => ProposalVote) private _proposalVotes;

// Original: contracts/18/contracts/governance/Governor.sol lines 47-47 state declaration
    mapping(uint256 => ProposalCore) private _proposals;
