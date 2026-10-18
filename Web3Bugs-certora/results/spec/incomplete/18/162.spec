// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/TimelockController.spec lines 47-49
// Target: TimelockController
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: TimelockController.spec:2-9
methods {
    getTimestamp(bytes32) returns(uint256) envfree
    _DONE_TIMESTAMP() returns(uint256) envfree
    isOperationPending(bytes32) returns(bool) envfree
}

invariant pendingCheck(bytes32 id)
    getTimestamp(id) > _DONE_TIMESTAMP() <=> isOperationPending(id)
filtered { f -> !f.isView }
