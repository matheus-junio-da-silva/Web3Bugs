// Source: contracts/7/specs/UserConfiguration.spec
// Literal property: invariant isUsingAsCollateralOrBorrowing, lines 81-82
// Literal dependency source lines: 1;4-6;16;81-82
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
    isUsingAsCollateralOrBorrowing(uint256) returns bool envfree
    isBorrowing(uint256) returns bool envfree
    isUsingAsCollateral(uint256) returns bool envfree
}

invariant isUsingAsCollateralOrBorrowing(uint256 reserveIndex ) 
	(isUsingAsCollateral(reserveIndex) || isBorrowing(reserveIndex)) <=>  isUsingAsCollateralOrBorrowing(reserveIndex)
