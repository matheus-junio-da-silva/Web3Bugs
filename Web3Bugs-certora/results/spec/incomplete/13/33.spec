// Project 13 — historical Notional Finance V2; original property is verbatim.
// Property: testAssetCash; instance 33; Status: incomplete.
// Original property: certora/asset/LiquidityCurve.spec:149-160
// Included original CVL ranges: certora/asset/LiquidityCurve.spec:7-7; certora/asset/LiquidityCurve.spec:11-11; certora/asset/LiquidityCurve.spec:149-160
// No migration to CVL2.

methods {
    getMarketAssetCash() returns (int256) envfree;
    executeTrade(uint256 timeToMaturity, int256 fCashToAccount) returns (int256,int256) envfree;
}

rule testAssetCash(int256 fCashToAccount, uint256 timeToMaturity){
    // require timeToMaturity <= 2^255-1;
    // require timeToMaturity > 0;
    // require fCashToAccount != 0;
    int256 marketAssetCashBefore = getMarketAssetCash();
    int256 assetCashToAccount;
    int256 assetCashToReserve;
    assetCashToAccount, assetCashToReserve = executeTrade(timeToMaturity, fCashToAccount);
    // require (assetCashToReserve > 0, "asset cash to reserve cannot be negative");
    int256 marketAssetCashAfter = getMarketAssetCash();
    assert marketAssetCashAfter > marketAssetCashBefore;
}
