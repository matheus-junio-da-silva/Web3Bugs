// Project 13: original historical CVL, Example 56
// Original source: certora/oldAccountContext.spec:83-94
// Included original CVL ranges: certora/oldAccountContext.spec:9-28;29-30;33-36;83-94; certora/oldAccountContext.spec:6-6
// CVL2 conversion intentionally out of scope

methods {
getActiveCurrencies(address account) returns (uint144) envfree
}

/* Unpack account context */
// definition unpackAccountNextSettleTime(bytes32 b) returns uint40 =
//     b & 0x00000000000000000000000000000000000000000000ffffffffffffffffffff;
// definition unpackAccountHasDebt(bytes32 b) returns bytes1 =
//     (b & 0x000000000000000000000000000000000000000000ff00000000000000000000) << 208;
// definition unpackAccountArrayLength(bytes32 b) returns uint8 =
//     (b & 0x0000000000000000000000000000000000000000ff0000000000000000000000) >> 48;
// definition unpackAccountBitmapId(bytes32 b) returns uint16 =
//     (b & 0x000000000000000000000000000000000000ffff000000000000000000000000) >> 56;
// definition unpackActiveCurrencies(bytes32 b) returns bytes18 =
//     (b & 0xffffffffffffffffffffffffffffffffffff0000000000000000000000000000) << 40;

// definition currencyActiveInPortfolio(uint16 c) returns bool = (c & 0x8000) == 0x8000;
// definition currencyActiveInBalances(uint16 c) returns bool = (c & 0x4000) == 0x4000;

/* Helper methods for active currencies */
// definition unmaskCurrency(uint144 c) returns uint144 = (c & 0x3FFF);
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
