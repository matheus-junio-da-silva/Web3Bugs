// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/TimelockController.spec lines 266-279
// Target: TimelockController
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: TimelockController.spec:6-14
methods {
    getMinDelay() returns(uint256) envfree
    hashOperation(address target, uint256 value, bytes data, bytes32 predecessor, bytes32 salt) returns(bytes32) envfree
    isOperationReady(bytes32) returns(bool)
    schedule(address, uint256, bytes32, bytes32, bytes32, uint256)
}

// Original CVL declaration: TimelockController.spec:27-30
function hashIdCorrelation(bytes32 id, address target, uint256 value, bytes data, bytes32 predecessor, bytes32 salt){
    require data.length < 32;
    require hashOperation(target, value, data, predecessor, salt) == id;
}

rule cooldown(method f, env e, env e2){
    bytes32 id;
    address target; uint256 value; bytes data ;bytes32 predecessor; bytes32 salt; uint256 delay;
    uint256 minDelay = getMinDelay();

    hashIdCorrelation(id, target, value, data, predecessor, salt);

    schedule(e, target, value, data, predecessor, salt, delay);

    calldataarg args;
    f(e, args);

    assert isOperationReady(e2, id) => (e2.block.timestamp - e.block.timestamp >= minDelay), "No rush! When I'm ready, I'm ready";
}
