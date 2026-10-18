// Project 13: original historical CVL, Example 55
// Original source: certora/oldAccountContext.spec:73-74
// Included original CVL ranges: certora/oldAccountContext.spec:4-4;5-5;73-74
// CVL2 conversion intentionally out of scope

methods {
getAssetArrayLength(address account) returns (uint8) envfree
getBitmapCurrency(address account) returns (uint16) envfree
}


invariant bitmapPortfoliosCannotHaveAssetArray(address account)
    getBitmapCurrency(account) != 0 => getAssetArrayLength(account) == 0
