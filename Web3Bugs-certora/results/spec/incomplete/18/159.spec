// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/RulesInProgress.spec lines 116-139
// Target: Governor (RulesInProgress; historical ERC20VotesHarness)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: RulesInProgress.spec:7-7
using ERC20VotesHarness as erc20votes

// Original CVL declaration: RulesInProgress.spec:10-13
methods {
    ghost_sum_vote_power_by_id(uint256) returns uint256 envfree
    proposalVotes(uint256) returns (uint256, uint256, uint256) envfree
}

// Original CVL declaration: GovernorBase.spec:5-5
using ERC20VotesHarness as erc20votes

// Original CVL declaration: GovernorBase.spec:8-28
methods {
    proposalSnapshot(uint256) returns uint256 envfree // matches proposalVoteStart
    castVote(uint256, uint8) returns uint256
    getPastTotalSupply(uint256) returns uint256 => DISPATCHER(true)
}

// Original CVL declaration: RulesInProgress.spec:40-42
hook Sstore ghost_sum_vote_power_by_id [KEY uint256 pId] uint256 current_power(uint256 old_power) STORAGE {
	havoc sum_all_votes_power assuming sum_all_votes_power@new() == sum_all_votes_power@old() - old_power + current_power;
}

// Original CVL declaration: RulesInProgress.spec:47-49
ghost tracked_weight(uint256) returns uint256 {
	init_state axiom forall uint256 p. tracked_weight(p) == 0;
}

// Original CVL declaration: RulesInProgress.spec:79-84
hook Sstore _proposalVotes [KEY uint256 pId].againstVotes uint256 votes(uint256 old_votes) STORAGE {
	havoc tracked_weight assuming forall uint256 p.(p == pId => tracked_weight@new(p) == tracked_weight@old(p) - old_votes + votes) &&
	                                            (p != pId => tracked_weight@new(p) == tracked_weight@old(p));
	havoc sum_tracked_weight assuming sum_tracked_weight@new() == sum_tracked_weight@old() - old_votes + votes;
    havoc votesAgainst assuming votesAgainst@new() == votesAgainst@old() - old_votes + votes;
}

// Original CVL declaration: RulesInProgress.spec:86-91
hook Sstore _proposalVotes [KEY uint256 pId].forVotes uint256 votes(uint256 old_votes) STORAGE {
	havoc tracked_weight assuming forall uint256 p.(p == pId => tracked_weight@new(p) == tracked_weight@old(p) - old_votes + votes) &&
	                                            (p != pId => tracked_weight@new(p) == tracked_weight@old(p));
	havoc sum_tracked_weight assuming sum_tracked_weight@new() == sum_tracked_weight@old() - old_votes + votes;
    havoc votesFor assuming votesFor@new() == votesFor@old() - old_votes + votes;
}

// Original CVL declaration: RulesInProgress.spec:93-98
hook Sstore _proposalVotes [KEY uint256 pId].abstainVotes uint256 votes(uint256 old_votes) STORAGE {
	havoc tracked_weight assuming forall uint256 p.(p == pId => tracked_weight@new(p) == tracked_weight@old(p) - old_votes + votes) &&
	                                            (p != pId => tracked_weight@new(p) == tracked_weight@old(p));
	havoc sum_tracked_weight assuming sum_tracked_weight@new() == sum_tracked_weight@old() - old_votes + votes;
    havoc votesAbstain assuming votesAbstain@new() == votesAbstain@old() - old_votes + votes;
}

// Original CVL declaration: RulesInProgress.spec:36-38
ghost sum_all_votes_power() returns uint256 {
	init_state axiom sum_all_votes_power() == 0;
}

// Original CVL declaration: RulesInProgress.spec:54-56
ghost sum_tracked_weight() returns uint256 {
	init_state axiom sum_tracked_weight() == 0;
}

// Original CVL declaration: RulesInProgress.spec:61-63
ghost votesAgainst() returns uint256 {
    init_state axiom votesAgainst() == 0;
}

// Original CVL declaration: RulesInProgress.spec:68-70
ghost votesFor() returns uint256 {
    init_state axiom votesFor() == 0;
}

// Original CVL declaration: RulesInProgress.spec:75-77
ghost votesAbstain() returns uint256 {
    init_state axiom votesAbstain() == 0;
}

rule possibleTotalVotes(uint256 pId, uint8 sup, env e, method f) {

    // add requireinvariant  for all i, j. i = i - 1 && i < j => checkpointlookup[i] < checkpointlookup[j];
    require tracked_weight(pId) <= erc20votes.getPastTotalSupply(e, proposalSnapshot(pId));

    uint256 againstB;
    uint256 forB;
    uint256 absatinB;
    againstB, forB, absatinB = proposalVotes(pId);

    calldataarg args;
    //f(e, args);

    castVote(e, pId, sup);

    uint256 against;
    uint256 for;
    uint256 absatin;
    against, for, absatin = proposalVotes(pId);

    uint256 ps = proposalSnapshot(pId);

    assert tracked_weight(pId) <= erc20votes.getPastTotalSupply(e, proposalSnapshot(pId)), "bla bla bla";
}
