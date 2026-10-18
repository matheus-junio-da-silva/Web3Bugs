// Source: contracts/13/contracts/mocks/certora/ValuationHarness.sol
// Original lines: 27-59
    }

    function calculateOracleRate(uint256 maturity, uint256 blockTime)
        external
        view
        returns (uint256)
    {
        return symbolicCashGroup.calculateOracleRate(maturity, blockTime);
    }

    function getMarketValues()
        external
        view
        returns (
            uint256 totalfCash,
            uint256 totalAssetCash,
            uint256 totalLiquidity,
            uint256 maturity
        )
    {
        require(symbolicMarket.totalfCash >= 0);
        require(symbolicMarket.totalAssetCash >= 0);
        require(symbolicMarket.totalLiquidity >= 0);

        totalfCash = uint256(symbolicMarket.totalfCash);
        totalAssetCash = uint256(symbolicMarket.totalAssetCash);
        totalLiquidity = uint256(symbolicMarket.totalLiquidity);
        maturity = symbolicMarket.maturity;
    }

    function getLiquidityHaircut(uint256 assetType) external view returns (uint256) {
        return symbolicCashGroup.getLiquidityHaircut(assetType);
    }

// Source: contracts/13/contracts/mocks/certora/ValuationHarness.sol
// Original lines: 35-67
    }

    function getMarketValues()
        external
        view
        returns (
            uint256 totalfCash,
            uint256 totalAssetCash,
            uint256 totalLiquidity,
            uint256 maturity
        )
    {
        require(symbolicMarket.totalfCash >= 0);
        require(symbolicMarket.totalAssetCash >= 0);
        require(symbolicMarket.totalLiquidity >= 0);

        totalfCash = uint256(symbolicMarket.totalfCash);
        totalAssetCash = uint256(symbolicMarket.totalAssetCash);
        totalLiquidity = uint256(symbolicMarket.totalLiquidity);
        maturity = symbolicMarket.maturity;
    }

    function getLiquidityHaircut(uint256 assetType) external view returns (uint256) {
        return symbolicCashGroup.getLiquidityHaircut(assetType);
    }

    function getPresentValue(
        int256 notional,
        uint256 maturity,
        uint256 blockTime,
        uint256 oracleRate
    ) external view returns (int256) {
        return AssetHandler.getPresentValue(notional, maturity, blockTime, oracleRate);
// Source: contracts/13/contracts/internal/valuation/AssetHandler.sol
// Original lines: 149-181

    /// @notice Returns the asset cash claim and the present value of the fCash asset (if it exists)
    function getLiquidityTokenValue(
        uint256 index,
        CashGroupParameters memory cashGroup,
        MarketParameters memory market,
        PortfolioAsset[] memory assets,
        uint256 blockTime,
        bool riskAdjusted
    ) internal view returns (int256, int256) {
        PortfolioAsset memory liquidityToken = assets[index];
        require(isLiquidityToken(liquidityToken.assetType) && liquidityToken.notional >= 0); // dev: get liquidity token value, not liquidity token

        {
            (uint256 marketIndex, bool idiosyncratic) =
                DateTime.getMarketIndex(
                    cashGroup.maxMarketIndex,
                    liquidityToken.maturity,
                    blockTime
                );
            // Liquidity tokens can never be idiosyncratic
            require(!idiosyncratic); // dev: idiosyncratic liquidity token

            // This market will always be initialized, if a liquidity token exists that means the market has some liquidity in it.
            cashGroup.loadMarket(market, marketIndex, true, blockTime);
        }

        int256 assetCashClaim;
        int256 fCashClaim;
        if (riskAdjusted) {
            (assetCashClaim, fCashClaim) = getHaircutCashClaims(liquidityToken, market, cashGroup);
        } else {
            (assetCashClaim, fCashClaim) = getCashClaims(liquidityToken, market);
