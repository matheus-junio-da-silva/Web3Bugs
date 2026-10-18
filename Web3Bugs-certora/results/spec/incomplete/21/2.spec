// Extracted literal original CVL declarations from contracts/21/specs/DSM.spec
methods{
getGuardianQuorum() returns (uint256) envfree
getGuardianLength() returns (uint256) envfree
}
        invariant quorumLeGuardian(env e, method f)
        getGuardianLength() >= getGuardianQuorum()
