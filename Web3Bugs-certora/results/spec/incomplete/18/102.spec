// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/GovernorBase.spec lines 116-120
// Target: Governor (historical ERC20VotesHarness)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: GovernorBase.spec:8-12
methods {
    proposalSnapshot(uint256) returns uint256 envfree // matches proposalVoteStart
    isCanceled(uint256) returns bool envfree
}

invariant canceledImplyStartAndEndDateNonZero(uint pId)
        isCanceled(pId) => proposalSnapshot(pId) != 0
        {preserved with (env e){               
                require e.block.number > 0;
        }}
