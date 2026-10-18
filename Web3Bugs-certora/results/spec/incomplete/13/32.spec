// Project 13 — historical Notional Finance V2; original property is verbatim.
// Property: executeTradeMovesImpliedRates; instance 32; Status: incomplete.
// Original property: certora/asset/LiquidityCurve.spec:100-147
// Included original CVL ranges: certora/asset/LiquidityCurve.spec:1-1; certora/asset/LiquidityCurve.spec:4-4; certora/asset/LiquidityCurve.spec:5-5; certora/asset/LiquidityCurve.spec:6-6; certora/asset/LiquidityCurve.spec:7-7; certora/asset/LiquidityCurve.spec:11-11; certora/asset/LiquidityCurve.spec:100-147
// No migration to CVL2.

methods {
    getRateScalar(uint256 timeToMaturity) returns (int256) envfree;
    getLastImpliedRate() returns (uint256) envfree;
    getPreviousTradeTime() returns (uint256) envfree;
    getMarketfCash() returns (int256) envfree;
    getMarketAssetCash() returns (int256) envfree;
    executeTrade(uint256 timeToMaturity, int256 fCashToAccount) returns (int256,int256) envfree;
}

rule executeTradeMovesImpliedRates(
    int256 fCashToAccount,
    uint256 timeToMaturity
) {
    env e;
    require fCashToAccount != 0;
    require getRateScalar(timeToMaturity) > 0;
    uint256 lastImpliedRate = getLastImpliedRate();
    int256 marketfCashBefore = getMarketfCash();
    int256 marketAssetCashBefore = getMarketAssetCash();
    int256 assetCashToAccount;
    int256 assetCashToReserve;

    assetCashToAccount, assetCashToReserve = executeTrade( timeToMaturity, fCashToAccount);
    require assetCashToAccount != 0 && assetCashToReserve != 0;
    require (fCashToAccount < 0 => lastImpliedRate > getLastImpliedRate(),"last trade rate did not move in correct direction");
    
    // assert fCashToAccount > 0 ? 
    //     // When fCashToAccount > 0 then lending, implied rates should decrease
    //     lastImpliedRate > getLastImpliedRate() :
    //     // When fCashToAccount < 0 then borrowing, implied rates should increase
    //     lastImpliedRate < getLastImpliedRate(),
    //     "last trade rate did not move in correct direction";

    require (fCashToAccount > 0 ? assetCashToAccount < 0 : assetCashToAccount > 0, "incorrect asset cash for fCash");
    int256 marketfCashAfter = getMarketfCash();
    int256 marketAssetCashAfter = getMarketAssetCash();
    require (assetCashToReserve >= 0, "asset cash to reserve cannot be negative");
    require (getPreviousTradeTime() < e.block.timestamp, "previous trade time did not update");
    // assert  to_mathint(marketfCashBefore) ==  to_mathint(fCashToAccount) + to_mathint(marketfCashAfter), "Market fCash does not net out";
   

    // require marketfCashBefore < 1000 &&
    //         marketAssetCashBefore < 1000 &&
    //         assetCashToAccount < 1000 &&
    //         assetCashToReserve < 1000 &&
    //         marketfCashAfter < 1000 &&
    //         marketAssetCashAfter < 1000;
            
    // Jeff's NEW VERSION assert getMarketAssetCash() == marketAssetCashBefore - assetCashToAccount - assetCashToReserve;
    // int256 a_minus_b_minus_c = to_int256(marketAssetCashBefore - assetCashToAccount - assetCashToReserve);
    // int256 a_minus_b_minus_c = to_int256(to_mathint(marketAssetCashBefore) - to_mathint(assetCashToAccount) - to_mathint(assetCashToReserve));
    // require a_minus_b_minus_c >= 0;
    // assert a_minus_b_minus_c == marketAssetCashAfter, //marketAssetCashBefore,
    //     "Market asset cash does not net out";
    assert to_mathint(marketAssetCashAfter) == to_mathint(marketAssetCashBefore) - to_mathint(assetCashToAccount) - to_mathint(assetCashToReserve), //marketAssetCashBefore,
        "Market asset cash does not net out";
}
