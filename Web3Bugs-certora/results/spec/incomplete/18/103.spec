// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/GovernorBase.spec lines 127-132
// Target: Governor (historical ERC20VotesHarness)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: GovernorBase.spec:8-11
methods {
    proposalSnapshot(uint256) returns uint256 envfree // matches proposalVoteStart
    proposalDeadline(uint256) returns uint256 envfree // matches proposalVoteEnd
    isExecuted(uint256) returns bool envfree
}

// Original CVL declaration: GovernorBase.spec:105-109
invariant startAndEndDatesNonZero(uint256 pId)
        proposalSnapshot(pId) != 0 <=> proposalDeadline(pId) != 0
        { preserved with (env e){   
                require e.block.number > 0;
        }}

invariant executedImplyStartAndEndDateNonZero(uint pId)
        isExecuted(pId) => proposalSnapshot(pId) != 0
        { preserved with (env e){
            requireInvariant startAndEndDatesNonZero(pId);
            require e.block.number > 0;
        }}
