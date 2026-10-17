// Source: contracts/7/specs/UserConfiguration.spec
// Literal property: invariant integrityOfEmpty, lines 134-135
// Literal dependency source lines: 1;4;10-11;16;134-135
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
    isUsingAsCollateralOrBorrowing(uint256) returns bool envfree
    isBorrowingAny() returns bool envfree
    isEmpty() returns bool envfree    
}

invariant integrityOfEmpty(uint256 reserveIndex) 
	 isEmpty() => !isBorrowingAny() && !isUsingAsCollateralOrBorrowing(reserveIndex)
