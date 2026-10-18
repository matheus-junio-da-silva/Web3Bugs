// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/GovernorBase.spec lines 138-146
// Target: Governor (historical ERC20VotesHarness)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: GovernorBase.spec:8-9
methods {
    proposalSnapshot(uint256) returns uint256 envfree // matches proposalVoteStart
    proposalDeadline(uint256) returns uint256 envfree // matches proposalVoteEnd
}

// Original CVL declaration: GovernorBase.spec:105-109
invariant startAndEndDatesNonZero(uint256 pId)
        proposalSnapshot(pId) != 0 <=> proposalDeadline(pId) != 0
        { preserved with (env e){   
                require e.block.number > 0;
        }}

invariant voteStartBeforeVoteEnd(uint256 pId)
        // from < to <= because snapshot and deadline can be the same block number if delays are set to 0
        // This is possible before the integration of GovernorSettings.sol to the system.
        // After integration of GovernorSettings.sol the invariant expression should be changed from <= to <
        (proposalSnapshot(pId) > 0 =>  proposalSnapshot(pId) <= proposalDeadline(pId))
        // (proposalSnapshot(pId) > 0 =>  proposalSnapshot(pId) <= proposalDeadline(pId))
        { preserved {
            requireInvariant startAndEndDatesNonZero(pId);
        }}
