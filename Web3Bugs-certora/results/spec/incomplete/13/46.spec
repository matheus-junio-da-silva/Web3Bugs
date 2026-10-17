// Project 13 — historical Notional Finance V2; original property is verbatim.
// Property: liquidityTokenValueMatchesClaims; instance 46; Status: incomplete.
// Original property: certora/asset/Valuation.spec:188-216
// Included original CVL ranges: certora/asset/Valuation.spec:41-41; certora/asset/Valuation.spec:42-42; certora/asset/Valuation.spec:46-46; certora/asset/Valuation.spec:188-216
// No migration to CVL2.

methods {
    calculateOracleRate(uint256 maturity, uint256 blockTime) returns (uint256) envfree;
    getMarketValues() returns (uint256, uint256, uint256, uint256) envfree;
    getLiquidityTokenValue(int256 fCashNotional, uint256 tokens, uint256 assetType, uint256 blockTime, bool riskAdjusted) returns (int256, int256) envfree;
}

rule liquidityTokenValueMatchesClaims(int256 fCashNotional, uint256 tokens, uint256 assetType) {
    env e;
    uint256 totalfCash;
    uint256 totalAssetCash;
    uint256 totalLiquidity;
    uint256 maturity;
    totalfCash, totalAssetCash, totalLiquidity, maturity = getMarketValues();
    require (totalLiquidity >= tokens);

    uint256 oracleRate;
    oracleRate = calculateOracleRate(maturity, e.block.timestamp);

    int assetCashClaim;
    int pv;

    assetCashClaim, pv = getLiquidityTokenValue(
        fCashNotional,
        tokens,
        assetType,
        e.block.timestamp,
        false // non risk adjusted
    );

    mathint netfCash = (totalfCash * tokens) / (totalLiquidity) + to_mathint(fCashNotional);
    mathint assetCash = (totalAssetCash * tokens) / (totalLiquidity);
    // TODO: need to convert to int somehow
    // assert pv == getPresentValue(netfCash, maturity, e.block.timestamp, oracleRate);
    assert to_mathint(assetCashClaim) == assetCash;
}
