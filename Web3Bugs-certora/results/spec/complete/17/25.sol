// Original: contracts/17/contracts/CToken.sol lines 408-414
     * @return The borrow interest rate per block, scaled by 1e18
     */
    function borrowRatePerBlock() external view returns (uint) {
        (uint opaqueErr, uint borrowRateMantissa) = interestRateModel.getBorrowRate(getCashPrior(), totalBorrows, totalReserves);
        require(opaqueErr == 0, "borrowRatePerBlock: interestRateModel.borrowRate failed"); // semi-opaque
        return borrowRateMantissa;
    }
