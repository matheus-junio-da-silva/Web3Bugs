// Source: contracts/7/specs/ReserveConfiguration.spec
// Literal property: rule setLiquidationThresholdIntegrity, lines 67-70
// Literal dependency source lines: 1;4-5;57;67-70
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
    setLiquidationThreshold(uint256) envfree
    getLiquidationThreshold() returns (uint256) envfree
}

rule setLiquidationThresholdIntegrity(uint256 threshold) {
    setLiquidationThreshold(threshold);
    assert getLiquidationThreshold() == threshold;
}
