// Source: contracts/7/specs/ReserveConfiguration.spec
// Literal property: rule setReserveFactorIntegrity, lines 127-130
// Literal dependency source lines: 1;24-25;57;127-130
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
    setReserveFactor(uint256) envfree
    getReserveFactor() returns (uint256) envfree
}

rule setReserveFactorIntegrity(uint256 reserveFactor) {
    setReserveFactor(reserveFactor);
    assert getReserveFactor() == reserveFactor;
}
