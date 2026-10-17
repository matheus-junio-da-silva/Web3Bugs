// Source: contracts/7/specs/UserConfiguration.spec
// Literal property: rule setUsingAsCollateral, lines 47-51
// Literal dependency source lines: 1;3;6;16;47-51
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
    setUsingAsCollateral(uint256, bool) envfree
    isUsingAsCollateral(uint256) returns bool envfree
}

rule  setUsingAsCollateral(uint256 reserveIndex, bool usingAsCollateral)
{
	setUsingAsCollateral(reserveIndex, usingAsCollateral);
	assert isUsingAsCollateral(reserveIndex) == usingAsCollateral;
}
