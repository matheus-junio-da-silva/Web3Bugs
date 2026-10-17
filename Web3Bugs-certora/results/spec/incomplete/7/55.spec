// Source: contracts/7/specs/UserConfiguration.spec
// Literal property: invariant integrityOfisBorrowingOne, lines 113-114
// Literal dependency source lines: 1;5;9;16;113-114
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
    isBorrowing(uint256) returns bool envfree
    isBorrowingOne() returns (bool) envfree
}

invariant integrityOfisBorrowingOne(uint256 reserveIndex, uint256 reserveIndexOther)
    isBorrowing(reserveIndex) && isBorrowingOne() => !isBorrowing(reserveIndexOther) || reserveIndexOther == reserveIndex
