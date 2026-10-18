// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/GovernorPreventLateQuorum.spec lines 186-214
// Target: GovernorPreventLateQuorumHarness
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: GovernorCountingSimple.spec:4-4
methods {
    ghost_sum_vote_power_by_id(uint256) returns uint256 envfree
}

// Original CVL declaration: GovernorBase.spec:8-26
methods {
    proposalSnapshot(uint256) returns uint256 envfree // matches proposalVoteStart
    hasVoted(uint256, address) returns bool
    castVote(uint256, uint8) returns uint256
    getVotes(address, uint256) returns uint256 => DISPATCHER(true)
}

// Original CVL declaration: GovernorPreventLateQuorum.spec:35-51
function helperFunctionsWithRevertOnlyCastVote(uint256 proposalId, method f, env e) {
    string reason; uint8 support; uint8 v; bytes32 r; bytes32 s; bytes params;
    if (f.selector == castVote(uint256, uint8).selector) {
		castVote@withrevert(e, proposalId, support);
	} else if  (f.selector == castVoteWithReason(uint256, uint8, string).selector) {
        castVoteWithReason@withrevert(e, proposalId, support, reason);
	} else if (f.selector == castVoteBySig(uint256, uint8,uint8, bytes32, bytes32).selector) {
		castVoteBySig@withrevert(e, proposalId, support, v, r, s);
	} else if (f.selector == castVoteWithReasonAndParamsBySig(uint256,uint8,string,bytes,uint8,bytes32,bytes32).selector) {
        castVoteWithReasonAndParamsBySig@withrevert(e, proposalId, support, reason, params, v, r, s);
    } else if (f.selector == castVoteWithReasonAndParams(uint256,uint8,string,bytes).selector) {
        castVoteWithReasonAndParams@withrevert(e, proposalId, support, reason, params);
    } else {
        calldataarg args;
        f@withrevert(e, args);
    }
}

// Original CVL declaration: GovernorCountingSimple.spec:31-33
hook Sstore ghost_sum_vote_power_by_id [KEY uint256 pId] uint256 current_power(uint256 old_power) STORAGE {
	havoc sum_all_votes_power assuming sum_all_votes_power@new() == sum_all_votes_power@old() - old_power + current_power;
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

// Original CVL declaration: GovernorCountingSimple.spec:38-40
ghost tracked_weight(uint256) returns uint256 {
	init_state axiom forall uint256 p. tracked_weight(p) == 0;
}

// Original CVL declaration: GovernorCountingSimple.spec:45-47
ghost sum_tracked_weight() returns uint256 {
	init_state axiom sum_tracked_weight() == 0;
}

rule hasVotedCorrelationNonzero(uint256 pId, method f, env e) filtered {f -> !f.isView} {
    address acc = e.msg.sender;

    require(getVotes(e, acc, proposalSnapshot(pId)) > 0); // assuming voter has non-zero voting power
    
    uint256 againstBefore = votesAgainst();
    uint256 forBefore = votesFor();
    uint256 abstainBefore = votesAbstain();

    bool hasVotedBefore = hasVoted(e, pId, acc);

    helperFunctionsWithRevertOnlyCastVote(pId, f, e); // should be f(e, args)

    uint256 againstAfter = votesAgainst();
    uint256 forAfter = votesFor();
    uint256 abstainAfter = votesAbstain();
    
    bool hasVotedAfter = hasVoted(e, pId, acc);

    // want all vote categories to not decrease and at least one category to increase
    assert 
        (!hasVotedBefore && hasVotedAfter) => 
        (againstBefore <= againstAfter && forBefore <= forAfter && abstainBefore <= abstainAfter), 
        "after a vote is cast, the number of votes for each category must not decrease"; // currently vacous but keeping for CI tests
    assert 
        (!hasVotedBefore && hasVotedAfter) => 
        (againstBefore < againstAfter || forBefore < forAfter || abstainBefore < abstainAfter),
        "after a vote is cast, the number of votes of at least one category must increase";
}
