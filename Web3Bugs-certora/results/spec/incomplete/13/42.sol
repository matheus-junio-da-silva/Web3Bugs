// Source: contracts/13/contracts/mocks/certora/ValuationHarness.sol
// Original lines: 59-91
    }

    function getPresentValue(
        int256 notional,
        uint256 maturity,
        uint256 blockTime,
        uint256 oracleRate
    ) external view returns (int256) {
        return AssetHandler.getPresentValue(notional, maturity, blockTime, oracleRate);
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