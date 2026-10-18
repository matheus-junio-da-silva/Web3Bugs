// Original: contracts/12/specs/UserConfiguration.spec lines 1;6;7;8;9;14-15
// Target: UserConfigurationHarness; original source property and method signatures kept verbatim.
// Not modernized to CVL2.
methods {
	isUsingAsCollateral(uint256) returns bool envfree
	isBorrowingAny() returns bool envfree
 	isEmpty() returns bool envfree
}

invariant notEmpty(uint256 reserveIndex) 
	(isBorrowingAny() ||  isUsingAsCollateral(reserveIndex)) => !isEmpty()
