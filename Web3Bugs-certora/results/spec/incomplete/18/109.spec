// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/GovernorBase.spec lines 230-242
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

rule noStartBeforeCreation(uint256 pId) {
    uint256 previousStart = proposalSnapshot(pId);
    // This line makes sure that we see only cases where start date is changed from 0, i.e. creation of proposal
    // We proved in immutableFieldsAfterProposalCreation that once dates set for proposal, it cannot be changed
    require !proposalCreated(pId); // previousStart == 0;
    
    env e; calldataarg args;
    propose(e, args);

    uint256 newStart = proposalSnapshot(pId);
    // if created, start is after current block number (creation block)
    assert(newStart != previousStart => newStart >= e.block.number);
}
