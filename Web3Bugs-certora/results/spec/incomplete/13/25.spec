// Project 13 Notional Finance V2; historical CVL retained verbatim.
// Property: getAndSetAccountContext; instance 25; Status: incomplete.
// Original property: certora/accountContext/SetAccountContext.spec:9-24
// Included original CVL ranges: certora/accountContext/SetAccountContext.spec:1-1; certora/accountContext/SetAccountContext.spec:3-3; certora/accountContext/SetAccountContext.spec:4-4; certora/accountContext/SetAccountContext.spec:5-5; certora/accountContext/SetAccountContext.spec:6-6; certora/accountContext/SetAccountContext.spec:9-24
// CVL1 era; no modernization or replacement assumptions.

methods {
    getNextSettleTime(address account) returns (uint40) envfree
    getHasDebt(address account) returns (uint8) envfree
    getAssetArrayLength(address account) returns (uint8) envfree
    getBitmapCurrency(address account) returns (uint16) envfree
    getActiveCurrencies(address account) returns (uint144) envfree
}

rule getAndSetAccountContext(
    address account,
    uint40 nextSettleTime,
    uint8 hasDebt,
    uint8 assetArrayLength,
    uint16 bitmapCurrencyId,
    uint144 activeCurrencies
) {
    env e;
    setAccountContext(e, account, nextSettleTime, hasDebt, assetArrayLength, bitmapCurrencyId, activeCurrencies);
    assert getNextSettleTime(account) == nextSettleTime, "next settle time does not match";
    assert getHasDebt(account) == hasDebt, "has debt does not match";
    assert getAssetArrayLength(account) == assetArrayLength, "asset array length does not match";
    assert getBitmapCurrency(account) == bitmapCurrencyId, "bitmap currency id does not match";
    assert getActiveCurrencies(account) == activeCurrencies, "active currencies does not match";
}
