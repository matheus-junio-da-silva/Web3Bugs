// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/TimelockController.spec lines 300-310
// Target: TimelockController
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: TimelockController.spec:2-15
methods {
    getTimestamp(bytes32) returns(uint256) envfree
    hashOperation(address target, uint256 value, bytes data, bytes32 predecessor, bytes32 salt) returns(bytes32) envfree
    execute(address, uint256, bytes, bytes32, bytes32)
}

// Original CVL declaration: TimelockController.spec:27-30
function hashIdCorrelation(bytes32 id, address target, uint256 value, bytes data, bytes32 predecessor, bytes32 salt){
    require data.length < 32;
    require hashOperation(target, value, data, predecessor, salt) == id;
}

rule executeChange(env e){
    bytes32 id;  bytes32 otherId; 
    address target; uint256 value; bytes data ;bytes32 predecessor; bytes32 salt;
    uint256 otherIdTimestampBefore = getTimestamp(otherId);

    hashIdCorrelation(id, target, value, data, predecessor, salt);

    execute(e, target, value, data, predecessor, salt);

    assert id != otherId => otherIdTimestampBefore == getTimestamp(otherId), "Master of puppets, I'm pulling your strings";
}
