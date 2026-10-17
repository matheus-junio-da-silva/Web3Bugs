// Source: contracts/7/specs/ReserveConfiguration.spec
// Literal property: rule setStableRateBorrowingEnabledIntegrity, lines 121-124
// Literal dependency source lines: 1;22-23;57;121-124
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
    setStableRateBorrowingEnabled(bool) envfree
    getStableRateBorrowingEnabled() returns (bool) envfree
}

rule setStableRateBorrowingEnabledIntegrity(bool enabled) {
    setStableRateBorrowingEnabled(enabled);
    assert getStableRateBorrowingEnabled() == enabled;
}
