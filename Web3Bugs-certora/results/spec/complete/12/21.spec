// Original: contracts/12/specs/UserConfiguration.spec lines 1;5;7;9;18-19
// Target: UserConfigurationHarness; original source property and method signatures kept verbatim.
// Not modernized to CVL2.
methods {
	isBorrowing(uint256) returns bool envfree
	isBorrowingAny() returns bool envfree
}

invariant borrowing(uint256 reserveIndex ) 
	 isBorrowing(reserveIndex) =>  isBorrowingAny() 
