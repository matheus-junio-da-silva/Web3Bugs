// Project 13: original historical CVL, Example 53
// Original source: certora/governance/GovernanceOwner.spec:5-12
// Included original CVL ranges: certora/governance/GovernanceOwner.spec:2-2;5-12
// CVL2 conversion intentionally out of scope

methods {
getOwner() returns address envfree
}


rule onlyOwnerCanUpdateGovernace(method f) filtered { f -> !f.isView } {
    env e;
    calldataarg arg;
    address ownerBefore = getOwner();
    // Any non reverting stateful call
    sinvoke f(e, arg);
    assert e.msg.sender == ownerBefore, "Non owner address invoked governance method";
}
