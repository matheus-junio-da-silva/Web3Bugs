// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/TimelockController.spec lines 245-261
// Target: TimelockController
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: TimelockController.spec:4-17
methods {
    PROPOSER_ROLE() returns(bytes32) envfree
    schedule(address, uint256, bytes32, bytes32, bytes32, uint256)
    _checkRole(bytes32) => DISPATCHER(true)
}

rule onlyProposer(method f, env e) filtered { f -> f.selector == schedule(address, uint256, bytes, bytes32, bytes32, uint256).selector
                                                    || f.selector == scheduleBatch(address[], uint256[], bytes[], bytes32, bytes32, uint256).selector } {
    bytes32 id;
    bytes32 role;
    address target; uint256 value; bytes data ;bytes32 predecessor; bytes32 salt; uint256 delay;

    _checkRole@withrevert(e, PROPOSER_ROLE());

    bool isCheckRoleReverted = lastReverted;

    calldataarg args;
    f@withrevert(e, args);

    bool isScheduleReverted = lastReverted;

    assert isCheckRoleReverted => isScheduleReverted, "Enemy was detected";
}
