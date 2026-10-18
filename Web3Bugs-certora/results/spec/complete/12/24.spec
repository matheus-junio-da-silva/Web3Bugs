// Original: contracts/12/specs/UserConfiguration.spec lines 1;2;5;6;9;34-44
// Target: UserConfigurationHarness; original source property and method signatures kept verbatim.
// Not modernized to CVL2.
methods {
	setBorrowing(uint256, bool) envfree
	isBorrowing(uint256) returns bool envfree
	isUsingAsCollateral(uint256) returns bool envfree
}

rule setBorrowingNoChangeToOther(uint256 reserveIndex, uint256 reserveIndexOther, bool borrowing)
{
	require reserveIndexOther != reserveIndex;
	require reserveIndexOther < 128 && reserveIndex < 128;
	bool otherReserveBorrowing =  isBorrowing(reserveIndexOther);
	bool otherReserveCollateral = isUsingAsCollateral(reserveIndexOther);

	setBorrowing(reserveIndex, borrowing);
	assert otherReserveBorrowing == isBorrowing(reserveIndexOther) &&
		otherReserveCollateral == isUsingAsCollateral(reserveIndexOther), "changed to other reserve";
}
