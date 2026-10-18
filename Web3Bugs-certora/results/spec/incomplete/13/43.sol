// Source: contracts/13/contracts/mocks/certora/ValuationHarness.sol
// Original lines: 68-100
    }

    function getRiskAdjustedPresentValue(
        int256 notional,
        uint256 maturity,
        uint256 blockTime,
        uint256 oracleRate
    ) external view returns (int256) {
        return
            AssetHandler.getRiskAdjustedPresentValue(
                symbolicCashGroup,
                notional,
                maturity,
                blockTime,
                oracleRate
            );
    }

    function getLiquidityTokenValue(
        int256 fCashNotional,
        uint256 tokens,
        uint256 assetType,
        uint256 blockTime,
        bool riskAdjusted
    ) external view returns (int256, int256) {
        require(tokens > 0 && tokens <= 2**255 - 1);

        PortfolioAsset[] memory assets;
        uint256 index;
        if (fCashNotional != 0) {
            assets = new PortfolioAsset[](2);
            assets[0].currencyId = 1;
            assets[0].assetType = Constants.FCASH_ASSET_TYPE;
