// Original: contracts/12/specs/UserConfiguration.spec lines 1;3;6;9;47-53
// Target: UserConfigurationHarness; original source property and method signatures kept verbatim.
// Not modernized to CVL2.
methods {
	setUsingAsCollateral(uint256, bool) envfree
	isUsingAsCollateral(uint256) returns bool envfree
}

rule  setUsingAsCollateral(uint256 reserveIndex, bool usingAsCollateral)
{
	require reserveIndex < 128;
	
	setUsingAsCollateral(reserveIndex, usingAsCollateral);
	assert isUsingAsCollateral(reserveIndex) == usingAsCollateral, "unexpected result";
}
