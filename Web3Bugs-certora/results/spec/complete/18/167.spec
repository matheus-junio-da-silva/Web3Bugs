// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/TimelockController.spec lines 106-116
// Target: TimelockController
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: TimelockController.spec:10-16
methods {
    isOperationDone(bytes32) returns(bool) envfree
    isOperationReady(bytes32) returns(bool)
    execute(address, uint256, bytes, bytes32, bytes32)
    executeBatch(address[], uint256[], bytes[], bytes32, bytes32)
}

rule readyDoneTransition(method f, env e){
    bytes32 id;

    require isOperationReady(e, id);

    calldataarg args;
    f(e, args);

    assert isOperationDone(id) => f.selector == execute(address, uint256, bytes, bytes32, bytes32).selector  
                                || f.selector == executeBatch(address[], uint256[], bytes[], bytes32, bytes32).selector , "It's not isOperationDone yet!";
}
