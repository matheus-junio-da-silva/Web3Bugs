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
// Original lines: 32-64
    /// this method will revert and the market must be initialized first.
    /// @return liquidityTokenAmount and net negative fCash
    function addLiquidity(MarketParameters storage market, int256 assetCash)
        internal
        returns (int256, int256)
    {
        require(market.totalLiquidity > 0, "M: zero liquidity");
        if (assetCash == 0) return (0, 0);
        require(assetCash > 0); // dev: negative asset cash

        int256 liquidityTokens = market.totalLiquidity.mul(assetCash).div(market.totalAssetCash);
        // No need to convert this to underlying, assetCash / totalAssetCash is a unitless proportion.
        int256 fCash = market.totalfCash.mul(assetCash).div(market.totalAssetCash);

        market.totalLiquidity = market.totalLiquidity.add(liquidityTokens);
        market.totalfCash = market.totalfCash.add(fCash);
        market.totalAssetCash = market.totalAssetCash.add(assetCash);
        market.storageState = updateLiquidity(market.storageState);
        // market.storageState = market.storageState | STORAGE_STATE_UPDATE_LIQUIDITY;

        return (liquidityTokens, fCash.neg());
    }

    /// @notice Remove liquidity from a market, assuming that it is initialized.
    /// @return asset cash and positive fCash claim to return
    function removeLiquidity(MarketParameters storage market, int256 tokensToRemove)
        internal
        returns (int256, int256)
    {
        if (tokensToRemove == 0) return (0, 0);
        require(tokensToRemove > 0); // dev: negative tokens to remove

        int256 assetCash = market.totalAssetCash.mul(tokensToRemove).div(market.totalLiquidity);