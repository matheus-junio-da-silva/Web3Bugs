// Project 13 — historical Notional Finance V2; original property is verbatim.
// Property: bitNumValidMaturitiesMustBeExact; instance 28; Status: incomplete.
// Original property: certora/asset/DateTime.spec:39-52
// Included original CVL ranges: certora/asset/DateTime.spec:1-1; certora/asset/DateTime.spec:4-4; certora/asset/DateTime.spec:9-9; certora/asset/DateTime.spec:11-11; certora/asset/DateTime.spec:13-13; certora/asset/DateTime.spec:15-15; certora/asset/DateTime.spec:39-52
// No migration to CVL2.

methods {
    getBitNumFromMaturity(uint256 blockTime, uint256 maturity) returns (uint256, bool) envfree
    isValidMaturity(uint256 maxMarketIndex, uint256 maturity, uint256 blockTime) returns (bool) envfree
}

definition MAX_TIMESTAMP() returns uint256 = 2^32 - 1;

definition MIN_TIMESTAMP() returns uint256 = 7776000;

definition MAX_MARKET_INDEX() returns uint256 = 7;

definition MAX_MARKET_MATURITY(uint256 blockTime) returns uint256 = blockTime + 20 * 86400 * 360;

rule bitNumValidMaturitiesMustBeExact(
    uint256 blockTime,
    uint256 maturity
) {
    // Respect time boundaries
    require MIN_TIMESTAMP() <= blockTime && blockTime <= MAX_TIMESTAMP();
    require MIN_TIMESTAMP() <= maturity && maturity <= MAX_TIMESTAMP();
    require isValidMaturity(MAX_MARKET_INDEX(), maturity, blockTime);
    bool isExact;
    _, isExact = getBitNumFromMaturity(blockTime, maturity);

    // BitNums go out a bit past the max 20 year maturity, those bits are not valid
    assert isExact && maturity <= MAX_MARKET_MATURITY(blockTime), "bitnum is valid does not match is valid maturity";
}
