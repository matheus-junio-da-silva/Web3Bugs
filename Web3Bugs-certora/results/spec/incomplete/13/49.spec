// Project 13 — historical Notional Finance V2; original property is verbatim.
// Property: ifCashNetPresentValueAccountsForAllAssets; instance 49; Status: incomplete.
// Original property: certora/asset/Valuation.spec:252-261
// Included original CVL ranges: certora/asset/Valuation.spec:50-50; certora/asset/Valuation.spec:51-51; certora/asset/Valuation.spec:252-261
// No migration to CVL2.

methods {
    getifCashNetPresentValue(address account, uint256 blockTime, bool riskAdjusted) returns (int256) envfree;
    getNumBitmapAssets(address account) returns (int256) envfree;
}

rule ifCashNetPresentValueAccountsForAllAssets(address account) {
    env e;
    // TODO: need to make these asumptions in the code
    // require calculateOracleRate == 0;
    // require getRiskAdjustedPresentValue == 1;

    // If each asset is valued at 1 then the total value should be the number of assets
    int256 underlyingPV = getifCashNetPresentValue(account, e.block.timestamp, true);
    assert underlyingPV == getNumBitmapAssets(account);
}
