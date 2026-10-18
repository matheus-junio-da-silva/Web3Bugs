// Project 13 Notional Finance V2; historical CVL retained verbatim.
// Property: enablingBitmapCannotLeaveBehindAssets; instance 4; Status: incomplete.
// Original property: certora/accountContext/ActiveCurrencies.spec:31-51
// Included original CVL ranges: certora/accountContext/ActiveCurrencies.spec:4-4; certora/accountContext/ActiveCurrencies.spec:5-5; certora/accountContext/ActiveCurrencies.spec:7-7; certora/accountContext/ActiveCurrencies.spec:22-22; certora/accountContext/ActiveCurrencies.spec:23-23; certora/accountContext/ActiveCurrencies.spec:25-25; certora/accountContext/ActiveCurrencies.spec:31-51
// CVL1 era; no modernization or replacement assumptions.

methods {
    getAssetArrayLength(address account) returns (uint8) envfree
    getBitmapCurrency(address account) returns (uint16) envfree
    getAssetsBitmap(address account) returns (uint256) envfree
}

definition MAX_CURRENCIES() returns uint256 = 0x3fff;

definition MAX_TIMESTAMP() returns uint256 = 2^32 - 1;

definition MIN_TIMESTAMP() returns uint256 = 7776000;

rule enablingBitmapCannotLeaveBehindAssets(address account, uint256 currencyId) {
    env e;
    require currencyId <= MAX_CURRENCIES();
    require e.block.timestamp >= MIN_TIMESTAMP();
    require e.block.timestamp <= MAX_TIMESTAMP();
    uint16 bitmapCurrencyId = getBitmapCurrency(account);
    uint8 assetArrayLength = getAssetArrayLength(account);
    uint256 assetsBitmap = getAssetsBitmap(account);
    require bitmapCurrencyId != 0 => assetArrayLength == 0;
    // Cannot set bitmap currency to 0 if it is already 0, will revert
    require bitmapCurrencyId == 0 => currencyId > 0;
    // Prevents invalid starting state
    require bitmapCurrencyId == 0 => assetsBitmap == 0x0000000000000000000000000000000000000000000000000000000000000000;

    enableBitmapForAccount@withrevert(e, account, currencyId, e.block.timestamp);
    // In these cases the account has active assets or cash debts
    assert (
        assetArrayLength != 0 ||
        assetsBitmap != 0x0000000000000000000000000000000000000000000000000000000000000000
    ) => lastReverted;
}
