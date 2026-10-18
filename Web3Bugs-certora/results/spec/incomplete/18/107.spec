// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/GovernorBase.spec lines 188-196
// Target: Governor (historical ERC20VotesHarness)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: GovernorBase.spec:14-15
methods {
    hasVoted(uint256, address) returns bool
    castVote(uint256, uint8) returns uint256
}

rule doubleVoting(uint256 pId, uint8 sup, method f) {
    env e;
    address user = e.msg.sender;        
    bool votedCheck = hasVoted(e, pId, user);

    castVote@withrevert(e, pId, sup);

    assert votedCheck => lastReverted, "double voting accured";
}
