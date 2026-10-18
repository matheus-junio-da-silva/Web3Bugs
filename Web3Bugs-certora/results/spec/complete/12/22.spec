// Original: contracts/12/specs/UserConfiguration.spec lines 1;4;5;6;9;21-22
// Target: UserConfigurationHarness; original source property and method signatures kept verbatim.
// Not modernized to CVL2.
methods {
	isUsingAsCollateralOrBorrowing(uint256) returns bool envfree
	isBorrowing(uint256) returns bool envfree
	isUsingAsCollateral(uint256) returns bool envfree
}

invariant collateralOrBorrowing(uint256 reserveIndex ) 
	(isUsingAsCollateral(reserveIndex) || isBorrowing(reserveIndex)) <=>  isUsingAsCollateralOrBorrowing(reserveIndex) 
