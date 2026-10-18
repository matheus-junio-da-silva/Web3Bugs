// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/GovernorBase.spec lines 254-261
// Target: Governor (historical ERC20VotesHarness)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: GovernorBase.spec:9-12
methods {
    proposalDeadline(uint256) returns uint256 envfree // matches proposalVoteEnd
    isExecuted(uint256) returns bool envfree
    isCanceled(uint256) returns bool envfree
}

rule noExecuteOrCancelBeforeDeadline(uint256 pId, method f){
    require !isExecuted(pId) && !isCanceled(pId);

    env e; calldataarg args;
    f(e, args);

    assert e.block.number < proposalDeadline(pId) => (!isExecuted(pId) && !isCanceled(pId)), "executed/cancelled before deadline";
}
