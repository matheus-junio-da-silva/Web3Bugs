// Project 13 Notional Finance V2; historical CVL retained verbatim.
// Property: nonZeroAssetArrayLength; instance 2; Status: incomplete.
// Original property: certora/accountContext/AccountPortfolio.spec:88-89
// Included original CVL ranges: certora/accountContext/AccountPortfolio.spec:4-4; certora/accountContext/AccountPortfolio.spec:5-5; certora/accountContext/AccountPortfolio.spec:88-89
// CVL1 era; no modernization or replacement assumptions.

methods {
    getAssetArrayLength(address account) returns (uint8) envfree
    getBitmapCurrency(address account) returns (uint16) envfree
}

invariant nonZeroAssetArrayLength(address account) 
      getAssetArrayLength(account) > 0 => getBitmapCurrency(account) == 0
