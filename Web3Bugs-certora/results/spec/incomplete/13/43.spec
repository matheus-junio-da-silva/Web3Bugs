// Project 13 — historical Notional Finance V2; original property is verbatim.
// Property: riskAdjustedPresentValueDecreasesForLongerMaturities; instance 43; Status: incomplete.
// Original property: certora/asset/Valuation.spec:120-134
// Included original CVL ranges: certora/asset/Valuation.spec:45-45; certora/asset/Valuation.spec:120-134
// No migration to CVL2.

methods {
    getRiskAdjustedPresentValue(int256 notional, uint256 maturity, uint256 blockTime, uint256 oracleRate) returns (int256) envfree;
}

rule riskAdjustedPresentValueDecreasesForLongerMaturities(
    int256 notional,
    uint256 maturity,
    uint256 maturityDelta,
    uint256 oracleRate
) {
    require notional != 0;
    env e;
    int256 shorterPV = getRiskAdjustedPresentValue(notional, maturity, e.block.timestamp, oracleRate);
    int256 longerPV = getRiskAdjustedPresentValue(notional, maturity + maturityDelta, e.block.timestamp, oracleRate);

    // PV cannot change signs as a result of this calculation
    assert notional > 0 => shorterPV > 0 && longerPV > 0 && shorterPV <= longerPV;
    assert notional < 0 => shorterPV < 0 && longerPV < 0 && longerPV <= shorterPV;
}
