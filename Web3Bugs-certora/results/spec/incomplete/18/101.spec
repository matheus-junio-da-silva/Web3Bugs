// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/GovernorBase.spec lines 105-109
// Target: Governor (historical ERC20VotesHarness)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: GovernorBase.spec:8-9
methods {
    proposalSnapshot(uint256) returns uint256 envfree // matches proposalVoteStart
    proposalDeadline(uint256) returns uint256 envfree // matches proposalVoteEnd
}

invariant startAndEndDatesNonZero(uint256 pId)
        proposalSnapshot(pId) != 0 <=> proposalDeadline(pId) != 0
        { preserved with (env e){   
                require e.block.number > 0;
        }}
