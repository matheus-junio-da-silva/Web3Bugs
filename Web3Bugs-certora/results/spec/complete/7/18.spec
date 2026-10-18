// Source: contracts/7/specs/ReserveConfiguration.spec
// Literal property: rule setFrozenIntegrity, lines 91-94
// Literal dependency source lines: 1;12-13;57;91-94
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
    setFrozen(bool) envfree
    getFrozen() returns (bool) envfree
}

rule setFrozenIntegrity(bool frozen) {
    setFrozen(frozen);
    assert getFrozen() == frozen;
}
