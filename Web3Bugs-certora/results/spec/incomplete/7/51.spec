// Source: contracts/7/specs/UserConfiguration.spec
// Literal property: rule setCollateralNoChangeToOther, lines 54-71
// Literal dependency source lines: 1;3;5-6;16;54-71
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
    setUsingAsCollateral(uint256, bool) envfree
    isBorrowing(uint256) returns bool envfree
    isUsingAsCollateral(uint256) returns bool envfree
}

rule setCollateralNoChangeToOther(uint256 reserveIndex, uint256 reserveIndexOther, bool usingAsCollateral)
{
    // reserveIndexOther info
	bool otherReserveBorrowingBefore =  isBorrowing(reserveIndexOther);
	bool otherReserveCollateralBefore = isUsingAsCollateral(reserveIndexOther);

	setUsingAsCollateral(reserveIndex, usingAsCollateral);
	
    // reserveIndex info
    bool ReserveBorrowingAfter =  isBorrowing(reserveIndex);
    // reserveIndexOther info
    bool otherReserveBorrowingAfter = isBorrowing(reserveIndexOther);
	bool otherReserveCollateralAfter = isUsingAsCollateral(reserveIndexOther);

    assert (reserveIndex != reserveIndexOther => 
                (otherReserveBorrowingAfter == otherReserveBorrowingBefore && 
                otherReserveCollateralAfter == otherReserveCollateralBefore));
}
