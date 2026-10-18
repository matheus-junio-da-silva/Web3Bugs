// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/GovernorBase.spec lines 152-158
// Target: Governor (historical ERC20VotesHarness)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: GovernorBase.spec:11-12
methods {
    isExecuted(uint256) returns bool envfree
    isCanceled(uint256) returns bool envfree
}

invariant noBothExecutedAndCanceled(uint256 pId) 
        !isExecuted(pId) || !isCanceled(pId)


/*
 * A proposal could be executed only if quorum was reached and vote succeeded
 */

