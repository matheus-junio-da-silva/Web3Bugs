// Source: contracts/7/specs/ReserveConfiguration.spec
// Literal property: rule setBorrowingEnabledIntegrity, lines 115-118
// Literal dependency source lines: 1;20-21;57;115-118
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
    setBorrowingEnabled(bool) envfree
    getBorrowingEnabled() returns (bool) envfree
}

rule setBorrowingEnabledIntegrity(bool enabled) {
    setBorrowingEnabled(enabled);
    assert getBorrowingEnabled() == enabled;
}
