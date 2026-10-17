// Source: contracts/7/specs/UserConfiguration.spec
// Literal property: invariant integrityOfisUsingAsCollateralAny, lines 103-104
// Literal dependency source lines: 1;6;8;16;103-104
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
    isUsingAsCollateral(uint256) returns bool envfree
    isUsingAsCollateralAny() returns bool envfree
}

invariant integrityOfisUsingAsCollateralAny(uint256 reserveIndex)
    isUsingAsCollateral(reserveIndex) => isUsingAsCollateralAny()
