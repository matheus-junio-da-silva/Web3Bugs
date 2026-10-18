// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/TimelockController.spec lines 199-209
// Target: TimelockController
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: TimelockController.spec:7-15
methods {
    hashOperation(address target, uint256 value, bytes data, bytes32 predecessor, bytes32 salt) returns(bytes32) envfree
    isOperation(bytes32) returns(bool) envfree
    execute(address, uint256, bytes, bytes32, bytes32)
}

// Original CVL declaration: TimelockController.spec:27-30
function hashIdCorrelation(bytes32 id, address target, uint256 value, bytes data, bytes32 predecessor, bytes32 salt){
    require data.length < 32;
    require hashOperation(target, value, data, predecessor, salt) == id;
}

rule executeRevertsFromUnset(method f, env e, env e2){
    address target; uint256 value; bytes data; bytes32 predecessor; bytes32 salt;
    bytes32 id;

    hashIdCorrelation(id, target, value, data, predecessor, salt);
    require !isOperation(id);

    execute@withrevert(e, target, value, data, predecessor, salt);

    assert lastReverted, "you go against execution nature";
}
