// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/TimelockController.spec lines 121-130
// Target: TimelockController
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: TimelockController.spec:8-13
methods {
    isOperation(bytes32) returns(bool) envfree
    isOperationPending(bytes32) returns(bool) envfree
    cancel(bytes32)
}

rule pendingCancelledTransition(method f, env e){
    bytes32 id;

    require isOperationPending(id);

    calldataarg args;
    f(e, args);

    assert !isOperation(id) => f.selector == cancel(bytes32).selector, "How you dare to cancel me?";
}
