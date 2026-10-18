// Source: contracts/7/specs/ReserveConfiguration.spec
// Literal property: rule setLiquidationBonusIntegrity, lines 73-76
// Literal dependency source lines: 1;6-7;57;73-76
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
    setLiquidationBonus(uint256) envfree
    getLiquidationBonus() returns (uint256) envfree
}

rule setLiquidationBonusIntegrity(uint256 bonus) {
    setLiquidationBonus(bonus);
    assert getLiquidationBonus() == bonus;
}
