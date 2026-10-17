// Project 13 Notional Finance V2; historical CVL retained verbatim.
// Property: integrityAssetArrayLength; instance 3; Status: incomplete.
// Original property: certora/accountContext/AccountPortfolio.spec:104-105
// Included original CVL ranges: certora/accountContext/AccountPortfolio.spec:4-4; certora/accountContext/AccountPortfolio.spec:15-15; certora/accountContext/AccountPortfolio.spec:104-105
// CVL1 era; no modernization or replacement assumptions.

methods {
    getAssetArrayLength(address account) returns (uint8) envfree
    getStoredAsset(address account, uint256 index)  returns (uint256) envfree
}

invariant integrityAssetArrayLength(address account, uint256 i) 
      getAssetArrayLength(account) > i <=> getStoredAsset(account,i) == 0
