// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: GovernorBase.spec:254-261 noExecuteOrCancelBeforeDeadline

// Original: contracts/18/contracts/governance/Governor.sol lines 189-191 function/modifier proposalDeadline
    function proposalDeadline(uint256 proposalId) public view virtual override returns (uint256) {
        return _proposals[proposalId].voteEnd.getDeadline();
    }

// Original: contracts/18/contracts/governance/Governor.sol lines 47-47 state declaration
    mapping(uint256 => ProposalCore) private _proposals;
