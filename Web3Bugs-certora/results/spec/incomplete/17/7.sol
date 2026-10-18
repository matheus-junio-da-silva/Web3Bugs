// Original: contracts/17/contracts/CToken.sol lines 595-661
      *      up to the current block and writes new checkpoint to storage.
      */
    function accrueInterest() public returns (uint) {
        AccrueInterestLocalVars memory vars;

        /* Calculate the current borrow interest rate */
        (vars.opaqueErr, vars.borrowRateMantissa) = interestRateModel.getBorrowRate(getCashPrior(), totalBorrows, totalReserves);
        require(vars.borrowRateMantissa <= borrowRateMaxMantissa, "borrow rate is absurdly high");
        if (vars.opaqueErr != 0) {
            return failOpaque(Error.INTEREST_RATE_MODEL_ERROR, FailureInfo.ACCRUE_INTEREST_BORROW_RATE_CALCULATION_FAILED, vars.opaqueErr);
        }

        /* Remember the initial block number */
        vars.currentBlockNumber = getBlockNumber();

        /* Calculate the number of blocks elapsed since the last accrual */
        (vars.mathErr, vars.blockDelta) = subUInt(vars.currentBlockNumber, accrualBlockNumber);
        assert(vars.mathErr == MathError.NO_ERROR); // Block delta should always succeed and if it doesn't, blow up.

        /*
         * Calculate the interest accumulated into borrows and reserves and the new index:
         *  simpleInterestFactor = borrowRate * blockDelta
         *  interestAccumulated = simpleInterestFactor * totalBorrows
         *  totalBorrowsNew = interestAccumulated + totalBorrows
         *  totalReservesNew = interestAccumulated * reserveFactor + totalReserves
         *  borrowIndexNew = simpleInterestFactor * borrowIndex + borrowIndex
         */
        (vars.mathErr, vars.simpleInterestFactor) = mulScalar(Exp({mantissa: vars.borrowRateMantissa}), vars.blockDelta);
        if (vars.mathErr != MathError.NO_ERROR) {
            return failOpaque(Error.MATH_ERROR, FailureInfo.ACCRUE_INTEREST_SIMPLE_INTEREST_FACTOR_CALCULATION_FAILED, uint(vars.mathErr));
        }

        (vars.mathErr, vars.interestAccumulated) = mulScalarTruncate(vars.simpleInterestFactor, totalBorrows);
        if (vars.mathErr != MathError.NO_ERROR) {
            return failOpaque(Error.MATH_ERROR, FailureInfo.ACCRUE_INTEREST_ACCUMULATED_INTEREST_CALCULATION_FAILED, uint(vars.mathErr));
        }

        (vars.mathErr, vars.totalBorrowsNew) = addUInt(vars.interestAccumulated, totalBorrows);
        if (vars.mathErr != MathError.NO_ERROR) {
            return failOpaque(Error.MATH_ERROR, FailureInfo.ACCRUE_INTEREST_NEW_TOTAL_BORROWS_CALCULATION_FAILED, uint(vars.mathErr));
        }

        (vars.mathErr, vars.totalReservesNew) = mulScalarTruncateAddUInt(Exp({mantissa: reserveFactorMantissa}), vars.interestAccumulated, totalReserves);
        if (vars.mathErr != MathError.NO_ERROR) {
            return failOpaque(Error.MATH_ERROR, FailureInfo.ACCRUE_INTEREST_NEW_TOTAL_RESERVES_CALCULATION_FAILED, uint(vars.mathErr));
        }

        (vars.mathErr, vars.borrowIndexNew) = mulScalarTruncateAddUInt(vars.simpleInterestFactor, borrowIndex, borrowIndex);
        if (vars.mathErr != MathError.NO_ERROR) {
            return failOpaque(Error.MATH_ERROR, FailureInfo.ACCRUE_INTEREST_NEW_BORROW_INDEX_CALCULATION_FAILED, uint(vars.mathErr));
        }

        /////////////////////////
        // EFFECTS & INTERACTIONS
        // (No safe failures beyond this point)

        /* We write the previously calculated values into storage */
        accrualBlockNumber = vars.currentBlockNumber;
        borrowIndex = vars.borrowIndexNew;
        totalBorrows = vars.totalBorrowsNew;
        totalReserves = vars.totalReservesNew;

        /* We emit an AccrueInterest event */
        emit AccrueInterest(vars.interestAccumulated, vars.borrowIndexNew, totalBorrows);

        return uint(Error.NO_ERROR);
    }

