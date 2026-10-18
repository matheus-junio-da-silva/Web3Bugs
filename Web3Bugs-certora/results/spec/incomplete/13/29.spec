// Project 13 — historical Notional Finance V2; original property is verbatim.
// Property: validMarketMaturitesHaveAnIndex; instance 29; Status: incomplete.
// Original property: certora/asset/DateTime.spec:57-71
// Included original CVL ranges: certora/asset/DateTime.spec:5-5; certora/asset/DateTime.spec:6-6; certora/asset/DateTime.spec:12-12; certora/asset/DateTime.spec:13-13; certora/asset/DateTime.spec:57-71
// No migration to CVL2.

methods {
    getMarketIndex(uint256 maxMarketIndex, uint256 maturity, uint256 blockTime) returns (uint256, bool) envfree
    isValidMarketMaturity(uint256 maxMarketIndex, uint256 maturity, uint256 blockTime) returns (bool) envfree
}

definition MIN_MARKET_INDEX() returns uint256 = 1;

definition MAX_MARKET_INDEX() returns uint256 = 7;

rule validMarketMaturitesHaveAnIndex(
    uint256 maxMarketIndex,
    uint256 maturity,
    uint256 blockTime
) {
    // Respect time boundaries
    uint256 marketIndex;
    bool isIdiosyncratic;
    marketIndex, isIdiosyncratic = getMarketIndex(maxMarketIndex, maturity, blockTime);
    bool isValidMarket = isValidMarketMaturity(maxMarketIndex, maturity, blockTime);

    // If a market is a valid market maturity then the getMarketIndex should agree
    assert isValidMarket <=> !isIdiosyncratic, "is valid market does not imply a market index";
    assert MIN_MARKET_INDEX() <= marketIndex && marketIndex <= MAX_MARKET_INDEX(), "market index out of boundaries";
}
