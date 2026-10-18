// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/GovernorPreventLateQuorum.spec lines 242-257
// Target: GovernorPreventLateQuorumHarness
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: GovernorPreventLateQuorum.spec:8-17
methods {
    lateQuorumVoteExtension() returns uint64 envfree
    getExtendedDeadlineIsUnset(uint256) returns bool envfree
    getExtendedDeadlineIsStarted(uint256) returns bool envfree
    getAgainstVotes(uint256) returns uint256 envfree
    getAbstainVotes(uint256) returns uint256 envfree
    getForVotes(uint256) returns uint256 envfree
}

// Original CVL declaration: GovernorCountingSimple.spec:4-4
methods {
    ghost_sum_vote_power_by_id(uint256) returns uint256 envfree
}

// Original CVL declaration: GovernorBase.spec:8-20
methods {
    proposalSnapshot(uint256) returns uint256 envfree // matches proposalVoteStart
    proposalDeadline(uint256) returns uint256 envfree // matches proposalVoteEnd
    updateQuorumNumerator(uint256)
    quorumReached(uint256) returns bool
}

// Original CVL declaration: GovernorPreventLateQuorum.spec:59-61
definition deadlineExtendable(env e, uint256 pId) returns bool = 
    getExtendedDeadlineIsUnset(pId) // deadline == 0
    && !quorumReached(e, pId);

// Original CVL declaration: GovernorPreventLateQuorum.spec:87-95
invariant quorumReachedEffect(env e, uint256 pId)
    quorumReached(e, pId) => proposalCreated(pId) // bug: 0 supply 0 votes => quorumReached
    // filtered { f -> f.selector != updateQuorumNumerator(uint256).selector } // * fails for this function

/*
 * I2: A non-existant proposal must meet the definition of one.
 * INVARIANT NOT PASSING // fails for updateQuorumNumerator and in the initial state when voting token total supply is 0 (causes quoromReached to return true)
 * ADVANCED SANITY NOT RAN
 */

// Original CVL declaration: GovernorPreventLateQuorum.spec:96-104
invariant proposalNotCreatedEffects(env e, uint256 pId)
    !proposalCreated(pId) => proposalNotCreated(e, pId)
    // filtered { f -> f.selector != updateQuorumNumerator(uint256).selector } // * fails for this function

/*
 * I3: A created propsal must be in state deadlineExtendable or deadlineExtended.
 * INVARIANT NOT PASSING // fails for updateQuorumNumerator and in the initial state when voting token total supply is 0 (causes quoromReached to return true)
 * ADVANCED SANITY NOT RAN 
 */

// Original CVL declaration: GovernorPreventLateQuorum.spec:105-108
invariant proposalInOneState(env e, uint256 pId) 
    proposalNotCreated(e, pId) || deadlineExtendable(e, pId) || deadlineExtended(e, pId)
    // filtered { f -> f.selector != updateQuorumNumerator(uint256).selector } // * fails for this function
    { preserved { requireInvariant proposalNotCreatedEffects(e, pId); }}

// Original CVL declaration: GovernorCountingSimple.spec:31-33
hook Sstore ghost_sum_vote_power_by_id [KEY uint256 pId] uint256 current_power(uint256 old_power) STORAGE {
	havoc sum_all_votes_power assuming sum_all_votes_power@new() == sum_all_votes_power@old() - old_power + current_power;
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

// Original CVL declaration: GovernorBase.spec:41-43
definition proposalCreated(uint256 pId) returns bool = 
    proposalSnapshot(pId) > 0
    && proposalDeadline(pId) > 0;

// Original CVL declaration: GovernorPreventLateQuorum.spec:64-66
definition deadlineExtended(env e, uint256 pId) returns bool = 
    getExtendedDeadlineIsStarted(pId) // deadline > 0
    && quorumReached(e, pId);

// Original CVL declaration: GovernorPreventLateQuorum.spec:68-75
definition proposalNotCreated(env e, uint256 pId) returns bool = 
    proposalSnapshot(pId) == 0
    && proposalDeadline(pId) == 0
    && getExtendedDeadlineIsUnset(pId)
    && getAgainstVotes(pId) == 0
    && getAbstainVotes(pId) == 0
    && getForVotes(pId) == 0
    && !quorumReached(e, pId);

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

rule deadlineExtenededIfQuorumReached(method f) filtered {f -> !f.isView} {
    env e; calldataarg args; uint256 pId;

    requireInvariant proposalInOneState(e, pId);
    requireInvariant quorumReachedEffect(e, pId); 
    requireInvariant proposalNotCreatedEffects(e, pId);

    bool wasDeadlineExtendable = deadlineExtendable(e, pId);
    uint64 extension = lateQuorumVoteExtension();
    uint256 deadlineBefore = proposalDeadline(pId);
    f(e, args);
    uint256 deadlineAfter = proposalDeadline(pId);
    
    assert deadlineAfter > deadlineBefore => wasDeadlineExtendable, "deadline must have been extendable for the deadline to be extended";
    assert deadlineAfter > deadlineBefore => deadlineBefore - e.block.number <= extension, "deadline extension should not be used";
}
