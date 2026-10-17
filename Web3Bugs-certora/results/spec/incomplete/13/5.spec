// Project 13 Notional Finance V2; historical CVL retained verbatim.
// Property: bitmapPortfoliosCannotHaveAssetArray; instance 5; Status: incomplete.
// Original property: certora/accountContext/ActiveCurrencies.spec:57-58
// Included original CVL ranges: certora/accountContext/ActiveCurrencies.spec:4-4; certora/accountContext/ActiveCurrencies.spec:5-5; certora/accountContext/ActiveCurrencies.spec:57-58
// CVL1 era; no modernization or replacement assumptions.

methods {
    getAssetArrayLength(address account) returns (uint8) envfree
    getBitmapCurrency(address account) returns (uint16) envfree
}

invariant bitmapPortfoliosCannotHaveAssetArray(address account)
    getBitmapCurrency(account) != 0 => getAssetArrayLength(account) == 0
