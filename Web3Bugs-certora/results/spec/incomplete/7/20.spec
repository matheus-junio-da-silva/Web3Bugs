// Source: contracts/7/specs/ReserveConfiguration.spec
// Literal property: rule setBorrowableInIsolationIntegrity, lines 103-106
// Literal dependency source lines: 1;16-17;57;103-106
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
    setBorrowableInIsolation(bool) envfree
    getBorrowableInIsolation() returns (bool) envfree
}

rule setBorrowableInIsolationIntegrity(bool borrowable) {
    setBorrowableInIsolation(borrowable);
    assert getBorrowableInIsolation() == borrowable;
}
