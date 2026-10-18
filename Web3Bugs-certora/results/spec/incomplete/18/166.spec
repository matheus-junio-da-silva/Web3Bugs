// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/TimelockController.spec lines 91-101
// Target: TimelockController
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: TimelockController.spec:8-14
methods {
    isOperation(bytes32) returns(bool) envfree
    isOperationPending(bytes32) returns(bool) envfree
    schedule(address, uint256, bytes32, bytes32, bytes32, uint256)
}

rule unsetPendingTransitionMethods(method f, env e){
    bytes32 id;

    require !isOperation(id);

    calldataarg args;
    f(e, args);

    assert isOperationPending(id) => (f.selector == schedule(address, uint256, bytes, bytes32, bytes32, uint256).selector 
                                || f.selector == scheduleBatch(address[], uint256[], bytes[], bytes32, bytes32, uint256).selector), "Why do we need to follow the schedule?";
}
