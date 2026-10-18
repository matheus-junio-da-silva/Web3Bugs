// Project 13 Notional Finance V2; historical CVL retained verbatim.
// Property: activeCurrenciesAreNotDuplicatedAndSorted; instance 6; Status: incomplete.
// Original property: certora/accountContext/ActiveCurrencies.spec:67-78
// Included original CVL ranges: certora/accountContext/ActiveCurrencies.spec:6-6; certora/accountContext/ActiveCurrencies.spec:11-12; certora/accountContext/ActiveCurrencies.spec:13-14; certora/accountContext/ActiveCurrencies.spec:17-20; certora/accountContext/ActiveCurrencies.spec:67-78
// CVL1 era; no modernization or replacement assumptions.

methods {
    getActiveCurrencies(address account) returns (uint144) envfree
}

definition getActiveMasked(address account, uint144 index) returns uint144 =
    (getActiveCurrencies(account) >> (128 - index * 16)) & 0x00000000000000000000000000000000ffff;

definition getActiveUnmasked(address account, uint144 index) returns uint144 =
    (getActiveCurrencies(account) >> (128 - index * 16)) & 0x000000000000000000000000000000003fff;

definition hasValidMask(address account, uint144 index) returns bool =
    (getActiveMasked(account, index) & 0x000000000000000000000000000000008000 == 0x000000000000000000000000000000008000) ||
    (getActiveMasked(account, index) & 0x000000000000000000000000000000004000 == 0x000000000000000000000000000000004000) ||
    (getActiveMasked(account, index) & 0x00000000000000000000000000000000c000 == 0x00000000000000000000000000000000c000);

invariant activeCurrenciesAreNotDuplicatedAndSorted(address account, uint144 i, uint144 j)
    (0 <= i && j == i + 1 && j < 9) =>
        // If the current slot is zero then the next slot must also be zero
        (
            getActiveMasked(account, i) == 0 ? getActiveMasked(account, j) == 0 :
                hasValidMask(account, i) && (
                    // The next slot may terminate
                    getActiveMasked(account, j) == 0 ||
                    // Or it may have a value which must be greater than the current value
                    (hasValidMask(account, j) && getActiveUnmasked(account, i) < getActiveUnmasked(account, j))
                )
        )
