// Project 13 — historical Notional Finance V2; original property is verbatim.
// Property: oracleRatesBlandedIntoRateWindow; instance 31; Status: incomplete.
// Original property: certora/asset/LiquidityCurve.spec:46-98
// Included original CVL ranges: certora/asset/LiquidityCurve.spec:1-1; certora/asset/LiquidityCurve.spec:3-3; certora/asset/LiquidityCurve.spec:4-4; certora/asset/LiquidityCurve.spec:5-5; certora/asset/LiquidityCurve.spec:9-9; certora/asset/LiquidityCurve.spec:11-11; certora/asset/LiquidityCurve.spec:12-12; certora/asset/LiquidityCurve.spec:46-98
// No migration to CVL2.

methods {
    getRateScalar(uint256 timeToMaturity) returns (int256) envfree;
    getRateOracleTimeWindow() returns (uint256) envfree;
    getLastImpliedRate() returns (uint256) envfree;
    getPreviousTradeTime() returns (uint256) envfree;
    getMarketOracleRate() returns (uint256) envfree;
    executeTrade(uint256 timeToMaturity, int256 fCashToAccount) returns (int256,int256) envfree;
    getStoredOracleRate() returns (uint256);
}

rule oracleRatesBlandedIntoRateWindow(method f){
env e;

uint marketOracleRate_1 = getMarketOracleRate();
uint lastImpliedRate_1 = getLastImpliedRate();
uint previousTradeTime_1 = getPreviousTradeTime();
uint rateOracleTimeWindow_1 = getRateOracleTimeWindow();
uint storedOracleRate_1 = getStoredOracleRate(e);

require e.block.timestamp > previousTradeTime_1;

// require (e.block.timestamp - previousTradeTime_1 > rateOracleTimeWindow_1 =>
        // marketOracleRate_1 == lastImpliedRate_1, "require 1_");
// require (e.block.timestamp - previousTradeTime_1 <= rateOracleTimeWindow_1 =>
        // isBetween(storedOracleRate_1,marketOracleRate_1,lastImpliedRate_1), "require 2_");

// calldataarg args;
// f(e,args);

    int256 fCashToAccount;
    uint256 timeToMaturity;
    int256 assetCashToAccount;
    int256 assetCashToReserve;
    require fCashToAccount != 0;
    require getRateScalar(timeToMaturity) > 0;

    assetCashToAccount,assetCashToReserve = executeTrade( timeToMaturity, fCashToAccount);
    require (assetCashToReserve >= 0, "asset cash to reserve cannot be negative");

uint marketOracleRate_2 = getMarketOracleRate();
uint lastImpliedRate_2 = getLastImpliedRate();
uint previousTradeTime_2 = getPreviousTradeTime();
uint rateOracleTimeWindow_2 = getRateOracleTimeWindow();
uint storedOracleRate_2 = getStoredOracleRate(e);

require (fCashToAccount < 0 => lastImpliedRate_1 > lastImpliedRate_2,"last trade rate did not move in correct direction");

// require 
//         lastImpliedRate_1 > 0 && lastImpliedRate_2 > 0 &&
//         marketOracleRate_1 > 0 && marketOracleRate_2 > 0 &&
//         previousTradeTime_1 > 0 && previousTradeTime_2 > 0 &&
//         rateOracleTimeWindow_1 > 0 && rateOracleTimeWindow_2 > 0 &&
//         storedOracleRate_1 > 0 && storedOracleRate_2 > 0;

require (e.block.timestamp > previousTradeTime_2, "previous trade time did not update");

require lastImpliedRate_2 != 0;

assert (e.block.timestamp - previousTradeTime_2 > rateOracleTimeWindow_2 =>
        marketOracleRate_2 == lastImpliedRate_2, "assert 1_");
// assert (e.block.timestamp - previousTradeTime_2 <= rateOracleTimeWindow_2 =>
        // isBetween(storedOracleRate_2,marketOracleRate_2,lastImpliedRate_2), "assert 2_");
}
