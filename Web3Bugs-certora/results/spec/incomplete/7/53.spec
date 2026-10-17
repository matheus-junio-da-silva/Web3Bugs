// Source: contracts/7/specs/UserConfiguration.spec
// Literal property: invariant integrityOfisUsingAsCollateralOne, lines 91-93
// Literal dependency source lines: 1;6-7;16;91-93
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
    isUsingAsCollateral(uint256) returns bool envfree
	isUsingAsCollateralOne() returns bool envfree
}

invariant integrityOfisUsingAsCollateralOne(uint256 reserveIndex, uint256 reserveIndexOther)
    isUsingAsCollateral(reserveIndex) && isUsingAsCollateralOne() => 
        !isUsingAsCollateral(reserveIndexOther) || reserveIndexOther == reserveIndex
