// Original: contracts/12/specs/UserConfiguration.spec lines 1;3;5;6;9;56-66
// Target: UserConfigurationHarness; original source property and method signatures kept verbatim.
// Not modernized to CVL2.
methods {
	setUsingAsCollateral(uint256, bool) envfree
	isBorrowing(uint256) returns bool envfree
	isUsingAsCollateral(uint256) returns bool envfree
}

rule setUsingAsCollateralNoChangeToOther(uint256 reserveIndex, uint256 reserveIndexOther, bool usingAsCollateral)
{
	require reserveIndexOther != reserveIndex;
	require reserveIndexOther < 128 && reserveIndex < 128;
	bool otherReserveBorrowing = isBorrowing(reserveIndexOther);
	bool otherReserveCollateral = isUsingAsCollateral(reserveIndexOther);
	
	setUsingAsCollateral(reserveIndex, usingAsCollateral);
	assert otherReserveBorrowing == isBorrowing(reserveIndexOther) &&
		otherReserveCollateral == isUsingAsCollateral(reserveIndexOther), "changed to other reserve";
}
