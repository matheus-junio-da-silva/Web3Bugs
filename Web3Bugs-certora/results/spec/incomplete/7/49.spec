// Source: contracts/7/specs/UserConfiguration.spec
// Literal property: rule setBorrowingNoChangeToOther, lines 27-44
// Literal dependency source lines: 1-2;5-6;16;27-44
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
    setBorrowing(uint256, bool) envfree
    isBorrowing(uint256) returns bool envfree
    isUsingAsCollateral(uint256) returns bool envfree
}

rule setBorrowingNoChangeToOther(uint256 reserveIndex, uint256 reserveIndexOther, bool borrowing)
{
    // reserveIndexOther info
	bool otherReserveBorrowingBefore =  isBorrowing(reserveIndexOther);
	bool otherReserveCollateralBefore = isUsingAsCollateral(reserveIndexOther);

	setBorrowing(reserveIndex, borrowing);
	
    // reserveIndex info
    bool ReserveBorrowingAfter =  isBorrowing(reserveIndex);
    // reserveIndexOther info
    bool otherReserveBorrowingAfter = isBorrowing(reserveIndexOther);
	bool otherReserveCollateralAfter = isUsingAsCollateral(reserveIndexOther);

    assert (reserveIndex != reserveIndexOther => 
                (otherReserveBorrowingAfter == otherReserveBorrowingBefore && 
                otherReserveCollateralAfter == otherReserveCollateralBefore));
}
