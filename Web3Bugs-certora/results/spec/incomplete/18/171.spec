// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/TimelockController.spec lines 169-179
// Target: TimelockController
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: TimelockController.spec:2-14
methods {
    getTimestamp(bytes32) returns(uint256) envfree
    hashOperation(address target, uint256 value, bytes data, bytes32 predecessor, bytes32 salt) returns(bytes32) envfree
    schedule(address, uint256, bytes32, bytes32, bytes32, uint256)
}

// Original CVL declaration: TimelockController.spec:27-30
function hashIdCorrelation(bytes32 id, address target, uint256 value, bytes data, bytes32 predecessor, bytes32 salt){
    require data.length < 32;
    require hashOperation(target, value, data, predecessor, salt) == id;
}

rule scheduleCheck(method f, env e){
    bytes32 id;

    address target; uint256 value; bytes data ;bytes32 predecessor; bytes32 salt; uint256 delay;

    hashIdCorrelation(id, target, value, data, predecessor, salt);

    schedule(e, target, value, data, predecessor, salt, delay);

    assert getTimestamp(id) == to_uint256(e.block.timestamp + delay), "Time doesn't obey to mortal souls";
}
