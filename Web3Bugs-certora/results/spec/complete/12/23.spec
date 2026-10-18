// Original: contracts/12/specs/UserConfiguration.spec lines 1;2;5;9;26-32
// Target: UserConfigurationHarness; original source property and method signatures kept verbatim.
// Not modernized to CVL2.
methods {
	setBorrowing(uint256, bool) envfree
	isBorrowing(uint256) returns bool envfree
}

rule setBorrowing(uint256 reserveIndex, bool borrowing)
{
	require reserveIndex < 128;
	
	setBorrowing(reserveIndex, borrowing);
	assert isBorrowing(reserveIndex) == borrowing, "unexpected result";
}
