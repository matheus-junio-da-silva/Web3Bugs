// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/TimelockController.spec lines 59-61
// Target: TimelockController
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: TimelockController.spec:2-10
methods {
    getTimestamp(bytes32) returns(uint256) envfree
    _DONE_TIMESTAMP() returns(uint256) envfree
    isOperationDone(bytes32) returns(bool) envfree
}

invariant doneCheck(bytes32 id)
    getTimestamp(id) == _DONE_TIMESTAMP() <=> isOperationDone(id)
filtered { f -> !f.isView }
