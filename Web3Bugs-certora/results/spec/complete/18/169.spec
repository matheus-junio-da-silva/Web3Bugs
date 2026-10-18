// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/TimelockController.spec lines 135-144
// Target: TimelockController
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: TimelockController.spec:10-10
methods {
    isOperationDone(bytes32) returns(bool) envfree
}

rule doneToNothingTransition(method f, env e){
    bytes32 id;

    require isOperationDone(id);

    calldataarg args;
    f(e, args);

    assert isOperationDone(id), "Did you find a way to escape? There is no way! HA-HA-HA";
}
