// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/RulesInProgress.spec lines 160-175
// Target: Governor (RulesInProgress; historical ERC20VotesHarness)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: RulesInProgress.spec:10-10
methods {
    ghost_sum_vote_power_by_id(uint256) returns uint256 envfree
}

// Original CVL declaration: GovernorBase.spec:13-13
methods {
    execute(address[], uint256[], bytes[], bytes32) returns uint256
}

// Original CVL declaration: RulesInProgress.spec:145-156
function executionsCall(method f, env e, address target, uint256 value, bytes data, 
                                    bytes32 predecessor, bytes32 salt, uint256 delay, 
                                    address[] targets, uint256[] values, bytes[] datas) {
    if  (f.selector == execute(address, uint256, bytes, bytes32, bytes32).selector) {
        execute(e, target, value, data, predecessor, salt);
	} else if (f.selector == executeBatch(address[], uint256[], bytes[], bytes32, bytes32).selector) {
        executeBatch(e, targets, values, datas, predecessor, salt);
	} else {
        calldataarg args;
        f(e, args);
    }
}

// Original CVL declaration: RulesInProgress.spec:40-42
hook Sstore ghost_sum_vote_power_by_id [KEY uint256 pId] uint256 current_power(uint256 old_power) STORAGE {
	havoc sum_all_votes_power assuming sum_all_votes_power@new() == sum_all_votes_power@old() - old_power + current_power;
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

// Original CVL declaration: RulesInProgress.spec:47-49
ghost tracked_weight(uint256) returns uint256 {
	init_state axiom forall uint256 p. tracked_weight(p) == 0;
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

rule getTimestampOnlyChange(method f, env e){
    bytes32 id;
    address target; uint256 value; bytes data; bytes32 predecessor; bytes32 salt; uint256 delay;
    address[] targets; uint256[] values; bytes[] datas;

    require (targets[0] == target && values[0] == value && datas[0] == data)
                || (targets[1] == target && values[1] == value && datas[1] == data)
                || (targets[2] == target && values[2] == value && datas[2] == data);

    hashIdCorrelation(id, target, value, data, predecessor, salt);

    executionsCall(f, e, target, value, data, predecessor, salt, delay, targets, values, datas);

    assert getTimestamp(id) == 1 => f.selector == execute(address, uint256, bytes, bytes32, bytes32).selector  
                                        || f.selector == executeBatch(address[], uint256[], bytes[], bytes32, bytes32).selector, "Did you find a way to break the system?";
}
