// Project 13 — historical Notional Finance V2; original property is verbatim.
// Property: calculateOracleRateIsBetweenOnChainRates; instance 41; Status: incomplete.
// Original property: certora/asset/Valuation.spec:82-98
// Included original CVL ranges: certora/asset/Valuation.spec:39-39; certora/asset/Valuation.spec:41-41; certora/asset/Valuation.spec:54-54; certora/asset/Valuation.spec:82-98
// No migration to CVL2.

methods {
    getMaturityAtMarketIndex(uint256 marketIndex, uint256 blockTime) returns (uint256) envfree;
    calculateOracleRate(uint256 maturity, uint256 blockTime) returns (uint256) envfree;
}

definition isBetween(uint256 x, uint256 y, uint256 z) returns bool = (y <= x && x <= z) || (z <= x && x <= y);

invariant calculateOracleRateIsBetweenOnChainRates(
    uint256 currencyId,
    uint256 maturity,
    uint256 shortMarketIndex,
    uint256 longMarketIndex,
    uint256 blockTime
)
    isBetween(
        maturity,
        getMaturityAtMarketIndex(shortMarketIndex, blockTime),
        getMaturityAtMarketIndex(longMarketIndex, blockTime)
    ) => 
    isBetween(
        calculateOracleRate(currencyId, maturity),
        calculateOracleRate(currencyId, getMaturityAtMarketIndex(shortMarketIndex, blockTime)),
        calculateOracleRate(currencyId, getMaturityAtMarketIndex(longMarketIndex, blockTime))
    )
