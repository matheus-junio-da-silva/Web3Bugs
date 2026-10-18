// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/TimelockController.spec lines 41-43
// Target: TimelockController
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: TimelockController.spec:2-8
methods {
    getTimestamp(bytes32) returns(uint256) envfree
    isOperation(bytes32) returns(bool) envfree
}

invariant operationCheck(bytes32 id)
    getTimestamp(id) > 0 <=> isOperation(id)
filtered { f -> !f.isView }
