// Project 13 — historical Notional Finance V2; original property is verbatim.
// Property: presentValueDecreasesForLongerMaturities; instance 42; Status: incomplete.
// Original property: certora/asset/Valuation.spec:103-117
// Included original CVL ranges: certora/asset/Valuation.spec:44-44; certora/asset/Valuation.spec:103-117
// No migration to CVL2.

methods {
    getPresentValue(int256 notional, uint256 maturity, uint256 blockTime, uint256 oracleRate) returns (int256) envfree;
}

rule presentValueDecreasesForLongerMaturities(
    int256 notional,
    uint256 maturity,
    uint256 maturityDelta,
    uint256 oracleRate
) {
    require notional != 0;
    env e;
    int256 shorterPV = getPresentValue(notional, maturity, e.block.timestamp, oracleRate);
    int256 longerPV = getPresentValue(notional, maturity + maturityDelta, e.block.timestamp, oracleRate);

    // Present value cannot change signs as a result of this calculation
    assert notional > 0 => shorterPV > 0 && longerPV > 0 && shorterPV <= longerPV;
    assert notional < 0 => shorterPV < 0 && longerPV < 0 && longerPV <= shorterPV;
}
