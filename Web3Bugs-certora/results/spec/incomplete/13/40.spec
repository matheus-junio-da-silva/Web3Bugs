// Project 13 — historical Notional Finance V2; original property is verbatim.
// Property: settlingBitmapAssetsDoesNotLoseTrack; instance 40; Status: incomplete.
// Original property: certora/asset/Settlement.spec:57-70
// Included original CVL ranges: certora/asset/Settlement.spec:1-1; certora/asset/Settlement.spec:5-5; certora/asset/Settlement.spec:7-7; certora/asset/Settlement.spec:57-70
// No migration to CVL2.

methods {
    getBitmapCurrencyId(address account) returns (uint256) envfree;
    getNumSettleableAssets(address account, uint256 blockTime) returns (uint256) envfree;
    getNumAssets(address account) returns (uint256) envfree;
}

rule settlingBitmapAssetsDoesNotLoseTrack(address account) {
    env e;
    // This is only true for bitmap currencies, it's mostly true for array portfolios but there
    // is an edge case where liquidity tokens net off against fCash exactly.
    require getBitmapCurrencyId(account) != 0;
    uint256 numAssets;
    uint256 numSettleAssets;
    numAssets = getNumAssets(account);
    numSettleAssets = getNumSettleableAssets(account, e.block.timestamp);

    settleAccount(e, account);
    assert getNumAssets(account) == numAssets - numSettleAssets;
    assert getNumSettleableAssets(account, e.block.timestamp) == 0;
}
