// Original: contracts/12/specs/UserConfiguration.spec lines 1;4;7;8;9;11-12
// Target: UserConfigurationHarness; original source property and method signatures kept verbatim.
// Not modernized to CVL2.
methods {
	isUsingAsCollateralOrBorrowing(uint256) returns bool envfree
	isBorrowingAny() returns bool envfree
 	isEmpty() returns bool envfree
}

invariant empty(uint256 reserveIndex) 
	 isEmpty() => !isBorrowingAny() && !isUsingAsCollateralOrBorrowing(reserveIndex)
