// Source: contracts/7/specs/UserConfiguration.spec
// Literal property: invariant integrityOfisBorrowingAny, lines 124-125
// Literal dependency source lines: 1;5;10;16;124-125
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
    isBorrowing(uint256) returns bool envfree
    isBorrowingAny() returns bool envfree
}

invariant integrityOfisBorrowingAny(uint256 reserveIndex)
    isBorrowing(reserveIndex) => isBorrowingAny()
