// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/AccessControl.spec lines 15-25
// Target: AccessControlMock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: AccessControl.spec:2-8
methods {
    grantRole(bytes32, address)
    _checkRole(bytes32)
    getRoleAdmin(bytes32) returns(bytes32) envfree
}

rule onlyRoleModifierCheckGrant(env e){
    bytes32 role; address account;

    _checkRole@withrevert(e, getRoleAdmin(role));
    bool checkRevert = lastReverted;

    grantRole@withrevert(e, role, account);
    bool grantRevert = lastReverted;

    assert checkRevert => grantRevert, "modifier goes bananas";
}
