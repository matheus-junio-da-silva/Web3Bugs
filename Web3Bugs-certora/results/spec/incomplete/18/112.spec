// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/GovernorBase.spec lines 308-326
// Target: Governor (historical ERC20VotesHarness)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: GovernorBase.spec:8-17
methods {
    proposalSnapshot(uint256) returns uint256 envfree // matches proposalVoteStart
    isExecuted(uint256) returns bool envfree
    isCanceled(uint256) returns bool envfree
    execute(address[], uint256[], bytes[], bytes32) returns uint256
    castVote(uint256, uint8) returns uint256
    updateQuorumNumerator(uint256)
    queue(address[], uint256[], bytes[], bytes32) returns uint256
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

// Original CVL declaration: GovernorBase.spec:116-120
invariant canceledImplyStartAndEndDateNonZero(uint pId)
        isCanceled(pId) => proposalSnapshot(pId) != 0
        {preserved with (env e){               
                require e.block.number > 0;
        }}

// Original CVL declaration: GovernorBase.spec:152-158
invariant noBothExecutedAndCanceled(uint256 pId) 
        !isExecuted(pId) || !isCanceled(pId)


/*
 * A proposal could be executed only if quorum was reached and vote succeeded
 */

rule allFunctionsRevertIfCanceled(method f) filtered {
    f -> !f.isView && !f.isFallback
      && f.selector != updateTimelock(address).selector
      && f.selector != updateQuorumNumerator(uint256).selector
      && f.selector != queue(address[],uint256[],bytes[],bytes32).selector
      && f.selector != relay(address,uint256,bytes).selector
      && f.selector != 0xb9a61961 // __acceptAdmin()
      && f.selector != setLateQuorumVoteExtension(uint64).selector
} {
    env e; calldataarg args;
    uint256 pId;
    require(isCanceled(pId));
    requireInvariant noBothExecutedAndCanceled(pId);
    requireInvariant canceledImplyStartAndEndDateNonZero(pId);

    helperFunctionsWithRevert(pId, f, e);

    assert(lastReverted, "Function was not reverted");
}
