// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/AccessControl.spec lines 62-74
// Target: AccessControlMock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: AccessControl.spec:3-9
methods {
    revokeRole(bytes32, address)
    hasRole(bytes32, address) returns(bool) envfree
}

rule revokeRoleEffect(env e){
    bytes32 role; address account; 
    bytes32 anotherRole; address nonEffectedAcc;
    require account != nonEffectedAcc;

    bool hasRoleBefore = hasRole(anotherRole, nonEffectedAcc);

    revokeRole(e, role, account);

    bool hasRoleAfter = hasRole(anotherRole, nonEffectedAcc);

    assert hasRoleBefore == hasRoleAfter, "modifier goes bananas";
}
