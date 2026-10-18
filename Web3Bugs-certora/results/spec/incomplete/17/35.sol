// Original: contracts/17/contracts/CToken.sol lines 418-444
     * @return The supply interest rate per block, scaled by 1e18
     */
    function supplyRatePerBlock() external view returns (uint) {
        /* We calculate the supply rate:
         *  underlying = totalSupply × exchangeRate
         *  borrowsPer = totalBorrows ÷ underlying
         *  supplyRate = borrowRate × (1-reserveFactor) × borrowsPer
         */
        uint exchangeRateMantissa = exchangeRateStored();

        (uint e0, uint borrowRateMantissa) = interestRateModel.getBorrowRate(getCashPrior(), totalBorrows, totalReserves);
        require(e0 == 0, "supplyRatePerBlock: calculating borrowRate failed"); // semi-opaque

        (MathError e1, Exp memory underlying) = mulScalar(Exp({mantissa: exchangeRateMantissa}), totalSupply);
        require(e1 == MathError.NO_ERROR, "supplyRatePerBlock: calculating underlying failed");

        (MathError e2, Exp memory borrowsPer) = divScalarByExp(totalBorrows, underlying);
        require(e2 == MathError.NO_ERROR, "supplyRatePerBlock: calculating borrowsPer failed");

        (MathError e3, Exp memory oneMinusReserveFactor) = subExp(Exp({mantissa: mantissaOne}), Exp({mantissa: reserveFactorMantissa}));
        require(e3 == MathError.NO_ERROR, "supplyRatePerBlock: calculating oneMinusReserveFactor failed");

        (MathError e4, Exp memory supplyRate) = mulExp3(Exp({mantissa: borrowRateMantissa}), oneMinusReserveFactor, borrowsPer);
        require(e4 == MathError.NO_ERROR, "supplyRatePerBlock: calculating supplyRate failed");

        return supplyRate.mantissa;
    }

