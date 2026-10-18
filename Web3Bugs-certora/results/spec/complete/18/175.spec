// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/TimelockController.spec lines 230-240
// Target: TimelockController
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: TimelockController.spec:8-10
methods {
    isOperation(bytes32) returns(bool) envfree
    isOperationDone(bytes32) returns(bool) envfree
}

rule cancelledNotExecuted(method f, env e){
    bytes32 id;

    require !isOperation(id);
    require e.block.timestamp > 1;

    calldataarg args;
    f(e, args);

    assert !isOperationDone(id), "The ship is not a creature of the air";
}
