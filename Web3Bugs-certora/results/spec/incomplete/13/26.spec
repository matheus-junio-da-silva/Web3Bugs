// Project 13 Notional Finance V2; historical CVL retained verbatim.
// Property: noChangeToOther; instance 26; Status: incomplete.
// Original property: certora/accountContext/SetAccountContext.spec:32-57
// Included original CVL ranges: certora/accountContext/SetAccountContext.spec:1-1; certora/accountContext/SetAccountContext.spec:3-3; certora/accountContext/SetAccountContext.spec:4-4; certora/accountContext/SetAccountContext.spec:5-5; certora/accountContext/SetAccountContext.spec:6-6; certora/accountContext/SetAccountContext.spec:32-57
// CVL1 era; no modernization or replacement assumptions.

methods {
    getNextSettleTime(address account) returns (uint40) envfree
    getHasDebt(address account) returns (uint8) envfree
    getAssetArrayLength(address account) returns (uint8) envfree
    getBitmapCurrency(address account) returns (uint16) envfree
    getActiveCurrencies(address account) returns (uint144) envfree
}

rule noChangeToOther(
    address account,
    uint40 nextSettleTime,
    uint8 hasDebt,
    uint8 assetArrayLength,
    uint16 bitmapCurrencyId,
    uint144 activeCurrencies
) {
    env e;
    address accountOther;
    require accountOther != account;
    require account != 0 && accountOther != 0;
    uint40 nextSettleTimeOther = getNextSettleTime(accountOther);
    uint8 hasDebtOther = getHasDebt(accountOther);
    uint8 assetArrayLengthOther = getAssetArrayLength(accountOther);
    uint16 bitmapCurrencyIdOther = getBitmapCurrency(accountOther);
    uint144 activeCurrenciesOther = getActiveCurrencies(accountOther);
        
    setAccountContext(e, account, nextSettleTime, hasDebt, assetArrayLength, bitmapCurrencyId, activeCurrencies);
    
    assert getNextSettleTime(accountOther) == nextSettleTimeOther, "next settle time does not match";
    assert getHasDebt(accountOther) == hasDebtOther, "has debt does not match";
    assert getAssetArrayLength(accountOther) == assetArrayLengthOther, "asset array length does not match";
    assert getBitmapCurrency(accountOther) == bitmapCurrencyIdOther, "bitmap currency id does not match";
    assert getActiveCurrencies(accountOther) == activeCurrenciesOther, "active currencies does not match";
}
