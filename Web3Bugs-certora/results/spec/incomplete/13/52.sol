// Project 13 example 52: original Solidity excerpt
// Source: contracts/13/contracts/mocks/certora/GovernanceActionHarness.sol
// Original lines: 72-100
            maxMarketIndex
        );
    }

    /// @notice Returns nToken address for a given currency
    function nTokenAddress(uint16 currencyId) external view returns (address) {
        return nTokenHandler.nTokenAddress(currencyId);
    }

    function getNTokenAccount(address tokenAddress)
        external
        view
        returns (bytes6 nTokenParameters, uint256 incentiveAnnualEmissionRate)
    {
        // prettier-ignore
        (
            /* currencyId */,
            /* totalSupply */,
            incentiveAnnualEmissionRate,
            /* lastInitializedTime */,
            nTokenParameters
        ) = nTokenHandler.getNTokenContext(tokenAddress);
    }

    /// @notice Returns address of contract owner
    function getOwner() external view returns (address) {
        return owner;
    }
}

// Source: contracts/13/contracts/external/actions/GovernanceAction.sol
// Original lines: 157-189
    /// denominated in WHOLE TOKENS (i.e. setting this to 1 means 1e8 tokens). The rate will not be
    /// exact due to multiplier effects and fluctuating token supply.
    function updateIncentiveEmissionRate(uint16 currencyId, uint32 newEmissionRate)
        external
        override
        onlyOwner
    {
        address nTokenAddress = nTokenHandler.nTokenAddress(currencyId);
        require(nTokenAddress != address(0), "Invalid currency");
        // Sanity check that emissions rate is not specified in 1e8 terms.
        require(newEmissionRate < Constants.INTERNAL_TOKEN_PRECISION, "Invalid rate");

        nTokenHandler.setIncentiveEmissionRate(nTokenAddress, newEmissionRate);
        emit UpdateIncentiveEmissionRate(currencyId, newEmissionRate);
    }

    /// @notice Updates collateralization parameters for an nToken
    /// @dev emit:UpdateTokenCollateralParameters
    /// @param currencyId the currency id that the nToken references
    /// @param residualPurchaseIncentive10BPS nTokens will have residual amounts of fCash at the end of each
    /// quarter that are "dead weight" because they are at idiosyncratic maturities and do not contribute to
    /// actively providing liquidity. This parameter will incentivize market participants to purchase these residuals
    /// at a discount from the on chain oracle rate, denominated in 10 basis point increments. These residuals will
    /// be added back into nToken balances and will be used to provide liquidity upon the next market initialization.
    /// @param pvHaircutPercentage a percentage (< 100) that the present value of the nToken's assets will be valued
    /// at for the purposes of free collateral, relevant when accounts hold nTokens as collateral against debts.
    /// @param residualPurchaseTimeBufferHours an arbitrage opportunity is available by pushing markets in one direction
    /// before quarterly settlement to generate large residual balances that can be purchased at a discount. The time buffer
    /// here ensures that anyone attempting such an act would have to wait some number of hours (likely a few days) before
    /// they could attempt to purchase residuals, ensuring that the market could realign to rates where the arbitrage is
    /// no longer possible.
    /// @param cashWithholdingBuffer10BPS nToken residuals may be negative fCash (debt), in this case cash is withheld to
    /// transfer to accounts that take on the debt. This parameter denominates the discounted rate at which the cash will
