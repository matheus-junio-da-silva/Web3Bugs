// Source: contracts/7/specs/UserConfiguration.spec
// Literal property: rule integrityOfSiloedBorrowingState, lines 154-159
// Literal dependency source lines: 1;9;13;16;154-159
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
    isBorrowingOne() returns (bool) envfree
    getSiloedBorrowingState() returns (bool, address) envfree
}

rule integrityOfSiloedBorrowingState(){
    bool existExactlyOneBorrow = isBorrowingOne();
    bool answer; address asset;
    answer, asset = getSiloedBorrowingState();
    assert answer => existExactlyOneBorrow;
}
