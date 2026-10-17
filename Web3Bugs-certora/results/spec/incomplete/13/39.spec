// Project 13 — historical Notional Finance V2; original property is verbatim.
// Property: settlementRatesAreNeverReset; instance 39; Status: incomplete.
// Original property: certora/asset/Settlement.spec:23-35
// Included original CVL ranges: certora/asset/Settlement.spec:3-3; certora/asset/Settlement.spec:23-35
// No migration to CVL2.

methods {
    getSettlementRate(uint256 currencyId, uint256 maturity) returns (int256) envfree;
}

rule settlementRatesAreNeverReset(address account, uint256 currencyId, uint256 maturity) {
    env e;
    require maturity < e.block.timestamp;
    // TODO: need to specify that the asset that is being settled exists at the maturity provided here.
    int256 settlementRateBefore = getSettlementRate(currencyId, maturity);
    settleAccount(e, account);
    int256 settlementRateAfter = getSettlementRate(currencyId, maturity);

    // Settlement rates must always be set after settling accounts
    assert settlementRateAfter > 0;
    // If settlement rates were set before, then they must not change after
    assert settlementRateBefore == 0 => settlementRateBefore == settlementRateAfter;
}
