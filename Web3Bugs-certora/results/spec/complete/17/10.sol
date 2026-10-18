// Original: contracts/17/contracts/CToken.sol lines 693-772
     * @return uint 0=success, otherwise a failure (see ErrorReporter.sol for details)
     */
    function mintFresh(address minter, uint mintAmount) internal returns (uint) {
        /* Fail if mint not allowed */
        uint allowed = comptroller.mintAllowed(address(this), minter, mintAmount);
        if (allowed != 0) {
            return failOpaque(Error.COMPTROLLER_REJECTION, FailureInfo.MINT_COMPTROLLER_REJECTION, allowed);
        }

        /* Verify market's block number equals current block number */
        if (accrualBlockNumber != getBlockNumber()) {
            return fail(Error.MARKET_NOT_FRESH, FailureInfo.MINT_FRESHNESS_CHECK);
        }

        MintLocalVars memory vars;

        /* Fail if checkTransferIn fails */
        vars.err = checkTransferIn(minter, mintAmount);
        if (vars.err != Error.NO_ERROR) {
            return fail(vars.err, FailureInfo.MINT_TRANSFER_IN_NOT_POSSIBLE);
        }

        /*
         * We get the current exchange rate and calculate the number of cTokens to be minted:
         *  mintTokens = mintAmount / exchangeRate
         */
        (vars.mathErr, vars.exchangeRateMantissa) = exchangeRateStoredInternal();
        if (vars.mathErr != MathError.NO_ERROR) {
            return failOpaque(Error.MATH_ERROR, FailureInfo.MINT_EXCHANGE_RATE_READ_FAILED, uint(vars.mathErr));
        }

        (vars.mathErr, vars.mintTokens) = divScalarByExpTruncate(mintAmount, Exp({mantissa: vars.exchangeRateMantissa}));
        if (vars.mathErr != MathError.NO_ERROR) {
            return failOpaque(Error.MATH_ERROR, FailureInfo.MINT_EXCHANGE_CALCULATION_FAILED, uint(vars.mathErr));
        }

        /*
         * We calculate the new total supply of cTokens and minter token balance, checking for overflow:
         *  totalSupplyNew = totalSupply + mintTokens
         *  accountTokensNew = accountTokens[minter] + mintTokens
         */
        (vars.mathErr, vars.totalSupplyNew) = addUInt(totalSupply, vars.mintTokens);
        if (vars.mathErr != MathError.NO_ERROR) {
            return failOpaque(Error.MATH_ERROR, FailureInfo.MINT_NEW_TOTAL_SUPPLY_CALCULATION_FAILED, uint(vars.mathErr));
        }

        (vars.mathErr, vars.accountTokensNew) = addUInt(accountTokens[minter], vars.mintTokens);
        if (vars.mathErr != MathError.NO_ERROR) {
            return failOpaque(Error.MATH_ERROR, FailureInfo.MINT_NEW_ACCOUNT_BALANCE_CALCULATION_FAILED, uint(vars.mathErr));
        }

        /////////////////////////
        // EFFECTS & INTERACTIONS
        // (No safe failures beyond this point)

        /*
         * We call doTransferIn for the minter and the mintAmount
         *  Note: The cToken must handle variations between ERC-20 and ETH underlying.
         *  On success, the cToken holds an additional mintAmount of cash.
         *  If doTransferIn fails despite the fact we checked pre-conditions,
         *   we revert because we can't be sure if side effects occurred.
         */
        vars.err = doTransferIn(minter, mintAmount);
        if (vars.err != Error.NO_ERROR) {
            return fail(vars.err, FailureInfo.MINT_TRANSFER_IN_FAILED);
        }

        /* We write previously calculated values into storage */
        totalSupply = vars.totalSupplyNew;
        accountTokens[minter] = vars.accountTokensNew;

        /* We emit a Mint event, and a Transfer event */
        emit Mint(minter, mintAmount, vars.mintTokens);
        emit Transfer(address(this), minter, vars.mintTokens);

        /* We call the defense hook */
        comptroller.mintVerify(address(this), minter, mintAmount, vars.mintTokens);

        return uint(Error.NO_ERROR);
    }

