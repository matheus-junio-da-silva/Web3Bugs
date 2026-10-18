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
