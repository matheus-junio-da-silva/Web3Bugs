// Project 13 Notional Finance V2; historical CVL retained verbatim.
// Property: bitmapCurrencyIsNotDuplicatedInActiveCurrencies; instance 7; Status: incomplete.
// Original property: certora/accountContext/ActiveCurrencies.spec:83-89
// Included original CVL ranges: certora/accountContext/ActiveCurrencies.spec:5-5; certora/accountContext/ActiveCurrencies.spec:6-6; certora/accountContext/ActiveCurrencies.spec:11-12; certora/accountContext/ActiveCurrencies.spec:13-14; certora/accountContext/ActiveCurrencies.spec:15-16; certora/accountContext/ActiveCurrencies.spec:83-89
// CVL1 era; no modernization or replacement assumptions.

methods {
    getBitmapCurrency(address account) returns (uint16) envfree
    getActiveCurrencies(address account) returns (uint144) envfree
}

definition getActiveMasked(address account, uint144 index) returns uint144 =
    (getActiveCurrencies(account) >> (128 - index * 16)) & 0x00000000000000000000000000000000ffff;

definition getActiveUnmasked(address account, uint144 index) returns uint144 =
    (getActiveCurrencies(account) >> (128 - index * 16)) & 0x000000000000000000000000000000003fff;

definition hasCurrencyMask(address account, uint144 index) returns bool =
    (getActiveMasked(account, index) & 0x000000000000000000000000000000004000 == 0x000000000000000000000000000000004000);

invariant bitmapCurrencyIsNotDuplicatedInActiveCurrencies(address account, uint144 i)
    0 <= i && i < 9 && getBitmapCurrency(account) != 0 &&
        (
            // When a bitmap is enable it can only have currency masks in the active currencies bytes
            (hasCurrencyMask(account, i) && getActiveUnmasked(account, i) == 0) ||
                getActiveMasked(account, i) == 0
        ) => getActiveUnmasked(account, i) != getBitmapCurrency(account)
