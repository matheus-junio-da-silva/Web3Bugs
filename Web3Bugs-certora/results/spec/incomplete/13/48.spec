// Project 13 — historical Notional Finance V2; original property is verbatim.
// Property: netCashGroupValueAccountsForAllAssets; instance 48; Status: incomplete.
// Original property: certora/asset/Valuation.spec:226-250
// Included original CVL ranges: certora/asset/Valuation.spec:48-48; certora/asset/Valuation.spec:49-49; certora/asset/Valuation.spec:226-250
// No migration to CVL2.

methods {
    getPortfolioCurrencyIdAtIndex(address account, uint256 index) returns (uint256) envfree;
    getNetCashGroupValue(address account, uint256 portfolioIndex, uint256 blockTime) returns (int256, uint256) envfree;
}

rule netCashGroupValueAccountsForAllAssets(
    address account,
    uint256 portfolioIndex
) {
    env e;
    // TODO: need to make these asumptions in the code
    // require getLiquidityTokenValue == 1
    // require calculateOracleRate == 0;
    // require getRiskAdjustedPresentValue == 1;
    // require assetRate == 0.02

    uint256 currencyId = getPortfolioCurrencyIdAtIndex(account, portfolioIndex);
    // Ensure that the portfolio index starts at a border between assets
    require portfolioIndex == 0 || getPortfolioCurrencyIdAtIndex(account, portfolioIndex - 1) != currencyId;
    int assetPV;
    uint newIndex;
    
    assetPV, newIndex = getNetCashGroupValue(account, portfolioIndex, e.block.timestamp);

    assert portfolioIndex < newIndex;
    assert getPortfolioCurrencyIdAtIndex(account, newIndex) != currencyId;
    // Every asset should be valued at 1 and the asset cash to pv conversion rate should be 50:1
    // so therefore the assetPV should equal the number of assets multiplied by 50
    assert to_mathint(assetPV) == (newIndex - portfolioIndex) * 50;
}
