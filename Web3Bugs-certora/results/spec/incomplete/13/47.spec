// Project 13 — historical Notional Finance V2; original property is verbatim.
// Property: portfolioIsAlwaysSorted; instance 47; Status: incomplete.
// Original property: certora/asset/Valuation.spec:219-222
// Included original CVL ranges: certora/asset/Valuation.spec:47-47; certora/asset/Valuation.spec:219-222
// No migration to CVL2.

methods {
    checkPortfolioSorted(address account) returns (bool) envfree;
}

invariant portfolioIsAlwaysSorted (address account)
    // Get portfolio from harness and test if assets are sorted, do this
    // inside a harness
    checkPortfolioSorted(account)
