// Source: contracts/7/specs/ReserveConfiguration.spec
// Literal property: rule setSiloedBorrowingIntegrity, lines 109-112
// Literal dependency source lines: 1;18-19;57;109-112
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
    setSiloedBorrowing(bool) envfree
    getSiloedBorrowing() envfree
}

rule setSiloedBorrowingIntegrity(bool siloed) {
    setSiloedBorrowing(siloed);
    assert getSiloedBorrowing() == siloed;
}
