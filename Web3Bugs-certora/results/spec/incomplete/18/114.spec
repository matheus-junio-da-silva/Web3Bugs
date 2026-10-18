// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/GovernorCountingSimple.spec lines 100-106
// Target: GovernorCountingSimple (historical governor harness)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: GovernorCountingSimple.spec:4-4
methods {
    ghost_sum_vote_power_by_id(uint256) returns uint256 envfree
}

// Original CVL declaration: GovernorCountingSimple.spec:31-33
hook Sstore ghost_sum_vote_power_by_id [KEY uint256 pId] uint256 current_power(uint256 old_power) STORAGE {
	havoc sum_all_votes_power assuming sum_all_votes_power@new() == sum_all_votes_power@old() - old_power + current_power;
}

// Original CVL declaration: GovernorCountingSimple.spec:38-40
ghost tracked_weight(uint256) returns uint256 {
	init_state axiom forall uint256 p. tracked_weight(p) == 0;
}

// Original CVL declaration: GovernorCountingSimple.spec:70-75
hook Sstore _proposalVotes [KEY uint256 pId].againstVotes uint256 votes(uint256 old_votes) STORAGE {
	havoc tracked_weight assuming forall uint256 p.(p == pId => tracked_weight@new(p) == tracked_weight@old(p) - old_votes + votes) &&
	                                            (p != pId => tracked_weight@new(p) == tracked_weight@old(p));
	havoc sum_tracked_weight assuming sum_tracked_weight@new() == sum_tracked_weight@old() - old_votes + votes;
    havoc votesAgainst assuming votesAgainst@new() == votesAgainst@old() - old_votes + votes;
}

// Original CVL declaration: GovernorCountingSimple.spec:77-82
hook Sstore _proposalVotes [KEY uint256 pId].forVotes uint256 votes(uint256 old_votes) STORAGE {
	havoc tracked_weight assuming forall uint256 p.(p == pId => tracked_weight@new(p) == tracked_weight@old(p) - old_votes + votes) &&
	                                            (p != pId => tracked_weight@new(p) == tracked_weight@old(p));
	havoc sum_tracked_weight assuming sum_tracked_weight@new() == sum_tracked_weight@old() - old_votes + votes;
    havoc votesFor assuming votesFor@new() == votesFor@old() - old_votes + votes;
}

// Original CVL declaration: GovernorCountingSimple.spec:84-89
hook Sstore _proposalVotes [KEY uint256 pId].abstainVotes uint256 votes(uint256 old_votes) STORAGE {
	havoc tracked_weight assuming forall uint256 p.(p == pId => tracked_weight@new(p) == tracked_weight@old(p) - old_votes + votes) &&
	                                            (p != pId => tracked_weight@new(p) == tracked_weight@old(p));
	havoc sum_tracked_weight assuming sum_tracked_weight@new() == sum_tracked_weight@old() - old_votes + votes;
    havoc votesAbstain assuming votesAbstain@new() == votesAbstain@old() - old_votes + votes;
}

// Original CVL declaration: GovernorCountingSimple.spec:27-29
ghost sum_all_votes_power() returns uint256 {
	init_state axiom sum_all_votes_power() == 0;
}

// Original CVL declaration: GovernorCountingSimple.spec:45-47
ghost sum_tracked_weight() returns uint256 {
	init_state axiom sum_tracked_weight() == 0;
}

// Original CVL declaration: GovernorCountingSimple.spec:52-54
ghost votesAgainst() returns uint256 {
    init_state axiom votesAgainst() == 0;
}

// Original CVL declaration: GovernorCountingSimple.spec:59-61
ghost votesFor() returns uint256 {
    init_state axiom votesFor() == 0;
}

// Original CVL declaration: GovernorCountingSimple.spec:66-68
ghost votesAbstain() returns uint256 {
    init_state axiom votesAbstain() == 0;
}

invariant SumOfVotesCastEqualSumOfPowerOfVotedPerProposal(uint256 pId) 
	tracked_weight(pId) == ghost_sum_vote_power_by_id(pId)


/*
 * sum of all votes casted is equal to the sum of voting power of those who voted
 */

