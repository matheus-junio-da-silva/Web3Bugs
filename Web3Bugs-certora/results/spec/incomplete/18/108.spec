// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/GovernorBase.spec lines 211-224
// Target: Governor (historical ERC20VotesHarness)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: GovernorBase.spec:8-9
methods {
    proposalSnapshot(uint256) returns uint256 envfree // matches proposalVoteStart
    proposalDeadline(uint256) returns uint256 envfree // matches proposalVoteEnd
}

// Original CVL declaration: GovernorBase.spec:41-43
definition proposalCreated(uint256 pId) returns bool = 
    proposalSnapshot(pId) > 0
    && proposalDeadline(pId) > 0;

rule immutableFieldsAfterProposalCreation(uint256 pId, method f) {
    uint256 _voteStart = proposalSnapshot(pId);
    uint256 _voteEnd = proposalDeadline(pId);

    require proposalCreated(pId); // startDate > 0
    
    env e; calldataarg arg;
    f(e, arg);

    uint256 voteStart_ = proposalSnapshot(pId);
    uint256 voteEnd_ = proposalDeadline(pId);
    assert _voteStart == voteStart_, "Start date was changed";
    assert _voteEnd == voteEnd_, "End date was changed";
}
