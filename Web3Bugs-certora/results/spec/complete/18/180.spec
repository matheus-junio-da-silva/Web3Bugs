// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/TimelockController.spec lines 315-323
// Target: TimelockController
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: TimelockController.spec:2-13
methods {
    getTimestamp(bytes32) returns(uint256) envfree
    cancel(bytes32)
}

rule cancelChange(env e){
    bytes32 id;  bytes32 otherId; 

    uint256 otherIdTimestampBefore = getTimestamp(otherId);

    cancel(e, id);

    assert id != otherId => otherIdTimestampBefore == getTimestamp(otherId), "Master of puppets, I'm pulling your strings";
}
