// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/AccessControl.spec lines 30-40
// Target: AccessControlMock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: AccessControl.spec:3-8
methods {
    revokeRole(bytes32, address)
    _checkRole(bytes32)
    getRoleAdmin(bytes32) returns(bytes32) envfree
}

rule onlyRoleModifierCheckRevoke(env e){
    bytes32 role; address account;

    _checkRole@withrevert(e, getRoleAdmin(role));
    bool checkRevert = lastReverted;

    revokeRole@withrevert(e, role, account);
    bool revokeRevert = lastReverted;

    assert checkRevert => revokeRevert, "modifier goes bananas";
}
