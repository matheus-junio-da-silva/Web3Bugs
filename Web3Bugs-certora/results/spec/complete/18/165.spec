// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/TimelockController.spec lines 76-86
// Target: TimelockController
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: TimelockController.spec:8-9
methods {
    isOperation(bytes32) returns(bool) envfree
    isOperationPending(bytes32) returns(bool) envfree
}

rule unsetPendingTransitionGeneral(method f, env e){
    bytes32 id;

    require !isOperation(id);
    require e.block.timestamp > 1;

    calldataarg args;
    f(e, args);

    assert isOperationPending(id) || !isOperation(id);
}
