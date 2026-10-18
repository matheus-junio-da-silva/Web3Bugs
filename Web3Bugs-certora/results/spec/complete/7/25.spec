// Source: contracts/7/specs/ReserveConfiguration.spec
// Literal property: rule setBorrowCapIntegrity, lines 133-136
// Literal dependency source lines: 1;26-27;57;133-136
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
    setBorrowCap(uint256) envfree
    getBorrowCap() returns (uint256) envfree
}

rule setBorrowCapIntegrity(uint256 borrowCap) {
    setBorrowCap(borrowCap);
    assert getBorrowCap() == borrowCap;
}
