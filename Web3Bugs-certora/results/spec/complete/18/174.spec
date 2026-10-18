// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/TimelockController.spec lines 214-225
// Target: TimelockController
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: TimelockController.spec:7-15
methods {
    hashOperation(address target, uint256 value, bytes data, bytes32 predecessor, bytes32 salt) returns(bytes32) envfree
    isOperationPending(bytes32) returns(bool) envfree
    isOperationReady(bytes32) returns(bool)
    execute(address, uint256, bytes, bytes32, bytes32)
}

// Original CVL declaration: TimelockController.spec:27-30
function hashIdCorrelation(bytes32 id, address target, uint256 value, bytes data, bytes32 predecessor, bytes32 salt){
    require data.length < 32;
    require hashOperation(target, value, data, predecessor, salt) == id;
}

rule executeRevertsEffectCheck(method f, env e){
    address target; uint256 value; bytes data; bytes32 predecessor; bytes32 salt;
    bytes32 id;

    hashIdCorrelation(id, target, value, data, predecessor, salt);
    require isOperationPending(id) && !isOperationReady(e, id);

    execute@withrevert(e, target, value, data, predecessor, salt);
    bool reverted = lastReverted;

    assert lastReverted => isOperationPending(id) && !isOperationReady(e, id), "you go against execution nature";
}
