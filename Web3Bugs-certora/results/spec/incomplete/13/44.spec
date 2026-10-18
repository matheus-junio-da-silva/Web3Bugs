// Project 13 — historical Notional Finance V2; original property is verbatim.
// Property: riskAdjustedPresentValueIsLessThanPresentValue; instance 44; Status: incomplete.
// Original property: certora/asset/Valuation.spec:138-149
// Included original CVL ranges: certora/asset/Valuation.spec:44-44; certora/asset/Valuation.spec:45-45; certora/asset/Valuation.spec:138-149
// No migration to CVL2.

methods {
    getPresentValue(int256 notional, uint256 maturity, uint256 blockTime, uint256 oracleRate) returns (int256) envfree;
    getRiskAdjustedPresentValue(int256 notional, uint256 maturity, uint256 blockTime, uint256 oracleRate) returns (int256) envfree;
}

rule riskAdjustedPresentValueIsLessThanPresentValue(
    int256 notional,
    uint256 maturity,
    uint256 oracleRate
) {
    require notional != 0;
    env e;
    int256 pv = getPresentValue(notional, maturity, e.block.timestamp, oracleRate);
    int256 riskAdjustedPV = getRiskAdjustedPresentValue(notional, maturity, e.block.timestamp, oracleRate);

    assert riskAdjustedPV <= pv;
}
