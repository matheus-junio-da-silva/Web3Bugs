// Source: contracts/13/contracts/mocks/certora/LiquidityCurveHarness.sol
// Original lines: 54-86
    }

    function getStoredOracleRate() external view returns (uint256) {
        uint256 settlementDate = DateTime.getReferenceTime(block.timestamp) + Constants.QUARTER;
        bytes32 marketSlot = Market.getMarketSlot(CURRENCY_ID, settlementDate, MATURITY);
        return Market.oracleRateStorage(marketSlot);
        
        // Instead we could write:
        // return symbolicMarkets[CURRENCY_ID][settlementDate][MATURITY].oracleRateStorage;


        // bytes32 slot = Market.getSlot(CURRENCY_ID, settlementDate, MATURITY);
        // bytes32 data;

        // assembly {
        //     data := sload(slot)
        // }

        // uint256 oracleRate = uint256(uint32(uint256(data >> 192)));

        // return oracleRate;
    }

    function getLastImpliedRate() external returns (uint256) {
        // uint256 settlementDate = _loadMarket();
         _loadMarket();
        // return symbolicMarkets[CURRENCY_ID][settlementDate][MATURITY].lastImpliedRate;
        // return _loadMarket().lastImpliedRate;
        return symbolicMarket.lastImpliedRate;
    }

    function getPreviousTradeTime() external returns (uint256) {
        // uint256 settlementDate = _loadMarket();

// Source: contracts/13/contracts/mocks/certora/LiquidityCurveHarness.sol
// Original lines: 75-107
    }

    function getLastImpliedRate() external returns (uint256) {
        // uint256 settlementDate = _loadMarket();
         _loadMarket();
        // return symbolicMarkets[CURRENCY_ID][settlementDate][MATURITY].lastImpliedRate;
        // return _loadMarket().lastImpliedRate;
        return symbolicMarket.lastImpliedRate;
    }

    function getPreviousTradeTime() external returns (uint256) {
        // uint256 settlementDate = _loadMarket();
         _loadMarket();
        // return symbolicMarkets[CURRENCY_ID][settlementDate][MATURITY].previousTradeTime;
        return symbolicMarket.previousTradeTime;
    }

    function getMarketOracleRate() external returns (uint256) {
        // uint256 settlementDate = _loadMarket();
         _loadMarket();
        // return symbolicMarkets[CURRENCY_ID][settlementDate][MATURITY].oracleRate;
        // return _loadMarket().oracleRate;
        return symbolicMarket.oracleRate;
    }

    function getMarketfCash() external returns (int256) {
        // uint256 settlementDate = _loadMarket();
         _loadMarket();
        // return symbolicMarkets[CURRENCY_ID][settlementDate][MATURITY].totalfCash;
        // return _loadMarket().totalfCash;
        return symbolicMarket.totalfCash;
    }


// Source: contracts/13/contracts/internal/markets/Market.sol
// Original lines: 55-87
    /// @notice Remove liquidity from a market, assuming that it is initialized.
    /// @return asset cash and positive fCash claim to return
    function removeLiquidity(MarketParameters storage market, int256 tokensToRemove)
        internal
        returns (int256, int256)
    {
        if (tokensToRemove == 0) return (0, 0);
        require(tokensToRemove > 0); // dev: negative tokens to remove

        int256 assetCash = market.totalAssetCash.mul(tokensToRemove).div(market.totalLiquidity);
        int256 fCash = market.totalfCash.mul(tokensToRemove).div(market.totalLiquidity);

        market.totalLiquidity = market.totalLiquidity.subNoNeg(tokensToRemove);
        market.totalfCash = market.totalfCash.subNoNeg(fCash);
        market.totalAssetCash = market.totalAssetCash.subNoNeg(assetCash);
        market.storageState = updateLiquidity(market.storageState);
        // market.storageState = market.storageState | STORAGE_STATE_UPDATE_LIQUIDITY;

        return (assetCash, fCash);
    }

    /// @notice Calculates the asset cash amount the results from trading fCashToAccount with the market. A positive
    /// fCashToAccount is equivalent of lending, a negative is borrowing. Updates the market state in memory.
    /// @param market the current market state
    /// @param cashGroup cash group configuration parameters
    /// @param fCashToAccount the fCash amount that will be deposited into the user's portfolio. The net change
    /// to the market is in the opposite direction.
    /// @param timeToMaturity number of seconds until maturity
    /// @return netAssetCash, netAssetCashToReserve
    function calculateTrade(
        MarketParameters storage market,
        CashGroupParameters storage cashGroup,
        int256 fCashToAccount,