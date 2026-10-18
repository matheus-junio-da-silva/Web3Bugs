// Project 13 — historical Notional Finance V2; original property is verbatim.
// Property: oracleRatesAreBlendedIntoTheRateWindow; instance 30; Status: incomplete.
// Original property: certora/asset/LiquidityCurve.spec:36-43
// Included original CVL ranges: certora/asset/LiquidityCurve.spec:3-3; certora/asset/LiquidityCurve.spec:4-4; certora/asset/LiquidityCurve.spec:5-5; certora/asset/LiquidityCurve.spec:9-9; certora/asset/LiquidityCurve.spec:12-12; certora/asset/LiquidityCurve.spec:27-27; certora/asset/LiquidityCurve.spec:36-43
// No migration to CVL2.

methods {
    getRateOracleTimeWindow() returns (uint256) envfree;
    getLastImpliedRate() returns (uint256) envfree;
    getPreviousTradeTime() returns (uint256) envfree;
    getMarketOracleRate() returns (uint256) envfree;
    getStoredOracleRate() returns (uint256);
}

definition isBetween(uint256 x, uint256 y, uint256 z) returns bool = (y <= x && x <= z) || (z <= x && x <= y);

invariant oracleRatesAreBlendedIntoTheRateWindow(env e)
    (e.block.timestamp - getPreviousTradeTime() > getRateOracleTimeWindow()) ?
        getMarketOracleRate() == getLastImpliedRate() :
        isBetween(
            getStoredOracleRate(e),
            getMarketOracleRate(),
            getLastImpliedRate()
        )
