// Project 13 — historical Notional Finance V2; original property is verbatim.
// Property: settleAssetsDeletesSettleableAssets; instance 38; Status: incomplete.
// Original property: certora/asset/Settlement.spec:13-17
// Included original CVL ranges: certora/asset/Settlement.spec:5-5; certora/asset/Settlement.spec:13-17
// No migration to CVL2.

methods {
    getNumSettleableAssets(address account, uint256 blockTime) returns (uint256) envfree;
}

rule settleAssetsDeletesSettleableAssets(address account) {
    env e;
    settleAccount(e, account);
    assert getNumSettleableAssets(account, e.block.timestamp) == 0;
}
