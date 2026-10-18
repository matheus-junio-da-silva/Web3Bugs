// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/TimelockController.spec lines 53-55
// Target: TimelockController
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: TimelockController.spec:2-12
methods {
    getTimestamp(bytes32) returns(uint256) envfree
    isOperationReady(bytes32) returns(bool)
}

invariant readyCheck(env e, bytes32 id)
    (e.block.timestamp >= getTimestamp(id) && getTimestamp(id) > 1) <=> isOperationReady(e, id)
filtered { f -> !f.isView }
