// Source: contracts/7/specs/ReserveConfiguration.spec
// Literal property: rule setLiquidationProtocolFeeIntegrity, lines 151-154
// Literal dependency source lines: 1;32-33;57;151-154
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
    setLiquidationProtocolFee(uint256) envfree
    getLiquidationProtocolFee() returns (uint256) envfree
}

rule setLiquidationProtocolFeeIntegrity(uint256 liquidationProtocolFee) {
    setLiquidationProtocolFee(liquidationProtocolFee);
    assert getLiquidationProtocolFee() == liquidationProtocolFee;
}
