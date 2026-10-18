// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/GovernorCountingSimple.spec lines 168-188
// Target: GovernorCountingSimple (historical governor harness)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: GovernorCountingSimple.spec:4-4
methods {
    ghost_sum_vote_power_by_id(uint256) returns uint256 envfree
}

// Original CVL declaration: GovernorBase.spec:13-17
methods {
    execute(address[], uint256[], bytes[], bytes32) returns uint256
    hasVoted(uint256, address) returns bool
    castVote(uint256, uint8) returns uint256
    queue(address[], uint256[], bytes[], bytes32) returns uint256
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

// Original CVL declaration: GovernorBase.spec:50-75
function helperFunctionsWithRevert(uint256 proposalId, method f, env e) {
    address[] targets; uint256[] values; bytes[] calldatas; string reason; bytes32 descriptionHash;
    uint8 support; uint8 v; bytes32 r; bytes32 s; bytes params;
	if (f.selector == propose(address[], uint256[], bytes[], string).selector) {
		uint256 result = propose@withrevert(e, targets, values, calldatas, reason);
        require(result == proposalId);
	} else if (f.selector == execute(address[], uint256[], bytes[], bytes32).selector) {
		uint256 result = execute@withrevert(e, targets, values, calldatas, descriptionHash);
        require(result == proposalId);
	} else if (f.selector == castVote(uint256, uint8).selector) {
		castVote@withrevert(e, proposalId, support);
	} else if  (f.selector == castVoteWithReason(uint256, uint8, string).selector) {
        castVoteWithReason@withrevert(e, proposalId, support, reason);
	} else if (f.selector == castVoteBySig(uint256, uint8,uint8, bytes32, bytes32).selector) {
		castVoteBySig@withrevert(e, proposalId, support, v, r, s);
    } else if (f.selector == queue(address[], uint256[], bytes[], bytes32).selector) {
        queue@withrevert(e, targets, values, calldatas, descriptionHash);
	} else if (f.selector == castVoteWithReasonAndParamsBySig(uint256,uint8,string,bytes,uint8,bytes32,bytes32).selector) {
        castVoteWithReasonAndParamsBySig@withrevert(e, proposalId, support, reason, params, v, r, s);
    } else if (f.selector == castVoteWithReasonAndParams(uint256,uint8,string,bytes).selector) {
        castVoteWithReasonAndParams@withrevert(e, proposalId, support, reason, params);
    } else {
        calldataarg args;
        f@withrevert(e, args);
    }
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

rule hasVotedCorrelation(uint256 pId, method f, env e, uint256 bn) {
    address acc = e.msg.sender;
    
    uint256 againstBefore = votesAgainst();
    uint256 forBefore = votesFor();
    uint256 abstainBefore = votesAbstain();

    bool hasVotedBefore = hasVoted(e, pId, acc);

    helperFunctionsWithRevert(pId, f, e);
    require(!lastReverted);

    uint256 againstAfter = votesAgainst();
    uint256 forAfter = votesFor();
    uint256 abstainAfter = votesAbstain();
    
    bool hasVotedAfter = hasVoted(e, pId, acc);

    // want all vote categories to not decrease and at least one category to increase
    assert (!hasVotedBefore && hasVotedAfter) => (againstBefore <= againstAfter && forBefore <= forAfter && abstainBefore <= abstainAfter), "no correlation: some category decreased";
}
