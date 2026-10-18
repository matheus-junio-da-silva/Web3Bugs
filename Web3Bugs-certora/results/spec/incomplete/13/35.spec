// Project 13 — historical Notional Finance V2; original property is verbatim.
// Property: impliedRatesDoNotChangeOnRemoveLiquidity; instance 35; Status: incomplete.
// Original property: certora/asset/LiquidityCurve.spec:195-231
// Included original CVL ranges: certora/asset/LiquidityCurve.spec:4-4; certora/asset/LiquidityCurve.spec:5-5; certora/asset/LiquidityCurve.spec:6-6; certora/asset/LiquidityCurve.spec:7-7; certora/asset/LiquidityCurve.spec:8-8; certora/asset/LiquidityCurve.spec:12-12; certora/asset/LiquidityCurve.spec:195-231
// No migration to CVL2.

methods {
    getLastImpliedRate() returns (uint256) envfree;
    getPreviousTradeTime() returns (uint256) envfree;
    getMarketfCash() returns (int256) envfree;
    getMarketAssetCash() returns (int256) envfree;
    getMarketLiquidity() returns (int256) envfree;
    getStoredOracleRate() returns (uint256);
}

rule impliedRatesDoNotChangeOnRemoveLiquidity(
    int256 tokenAmount
) {
    env e;
    require tokenAmount > 0;
    uint256 previousTradeTime = getPreviousTradeTime();
    uint256 oracleRate = getStoredOracleRate(e);
    uint256 lastImpliedRate = getLastImpliedRate();
    int256 marketfCashBefore = getMarketfCash();
    int256 marketAssetCashBefore = getMarketAssetCash();
    int256 marketLiquidityBefore = getMarketLiquidity();
    require marketfCashBefore >= 0 && marketfCashBefore <= to_int256(2^80 - 1);
    require marketAssetCashBefore >= 0 && marketAssetCashBefore <= to_int256(2^80 - 1);
    require marketLiquidityBefore >= 0 && marketLiquidityBefore <= to_int256(2^80 - 1);
    require previousTradeTime >= 0 && previousTradeTime <= 2^32 - 1;
    require lastImpliedRate >= 0 && lastImpliedRate <= 2^32 - 1;
    require oracleRate >= 0 && oracleRate <= 2^32 - 1;

    require marketLiquidityBefore >= tokenAmount;

    int256 assetCash;
    int256 fCashToAccount;
    assetCash, fCashToAccount = removeLiquidity(e, tokenAmount);

    require fCashToAccount != 0;

    int256 marketfCashAfter = getMarketfCash();
    int256 marketAssetCashAfter = getMarketAssetCash();
    int256 marketLiquidityAfter = getMarketLiquidity();
    uint256 previousTradeTimeAfter = getPreviousTradeTime();
    uint256 lastImpliedRateAfter = getLastImpliedRate();
    assert to_mathint(marketAssetCashBefore) - to_mathint(assetCash) == to_mathint(marketAssetCashAfter), "market asset cash imbalance";
    assert to_mathint(marketfCashBefore) - to_mathint(fCashToAccount) == to_mathint(marketfCashAfter), "fCash imbalance";
    assert to_mathint(marketLiquidityBefore) - to_mathint(tokenAmount) == to_mathint(marketLiquidityAfter), "liquidity token imbalance";
    assert previousTradeTimeAfter == previousTradeTime, "previous trade time did update";
    assert lastImpliedRateAfter == lastImpliedRate, "last trade rate did update";
}
