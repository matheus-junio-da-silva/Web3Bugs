// Project 13 — historical Notional Finance V2; original property is verbatim.
// Property: bitNumAndMaturitiesMustMatch; instance 27; Status: incomplete.
// Original property: certora/asset/DateTime.spec:21-33
// Included original CVL ranges: certora/asset/DateTime.spec:1-1; certora/asset/DateTime.spec:3-3; certora/asset/DateTime.spec:21-33
// No migration to CVL2.

methods {
    getBitNumFromMaturity(uint256 blockTime, uint256 maturity) returns (uint256, bool) envfree
    getMaturityFromBitNum(uint256 blockTime, uint256 bitNum) returns (uint256) envfree
}

rule bitNumAndMaturitiesMustMatch(
    uint256 blockTime,
    uint256 maturity
) {
    // Respect time boundaries
    uint256 bitNum;
    bool isExact;
    bitNum, isExact = getBitNumFromMaturity(blockTime, maturity);
    uint256 calculatedMaturity = getMaturityFromBitNum(blockTime, bitNum);

    // If the bitnum is not exact then the calculated maturity will not match
    assert isExact => maturity == calculatedMaturity, "maturity does not match calculated maturity";
}
