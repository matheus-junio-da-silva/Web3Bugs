// Source: contracts/7/specs/ReserveConfiguration.spec
// Literal property: rule setActiveIntegrity, lines 85-88
// Literal dependency source lines: 1;10-11;57;85-88
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
    setActive(bool) envfree
    getActive() returns (bool) envfree
}

rule setActiveIntegrity(bool active) {
    setActive(active);
    assert getActive() == active;
}
