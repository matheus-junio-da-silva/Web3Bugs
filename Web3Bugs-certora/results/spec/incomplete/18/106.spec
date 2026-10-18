// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/GovernorBase.spec lines 159-169
// Target: Governor (historical ERC20VotesHarness)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: GovernorBase.spec:11-21
methods {
    isExecuted(uint256) returns bool envfree
    quorumReached(uint256) returns bool
    voteSucceeded(uint256) returns bool envfree
}

rule executionOnlyIfQuoromReachedAndVoteSucceeded(uint256 pId, env e, method f){
    bool isExecutedBefore = isExecuted(pId);
    bool quorumReachedBefore = quorumReached(e, pId);
    bool voteSucceededBefore = voteSucceeded(pId);
    
    calldataarg args;
    f(e, args);
    
    bool isExecutedAfter = isExecuted(pId);
    assert (!isExecutedBefore && isExecutedAfter) => (quorumReachedBefore && voteSucceededBefore), "quorum was changed";
}
