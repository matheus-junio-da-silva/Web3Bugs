// Source: contracts/7/specs/ReserveConfiguration.spec
// Literal property: rule setDebtCeilingIntegrity, lines 145-148
// Literal dependency source lines: 1;30-31;57;145-148
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
    setDebtCeiling(uint256) envfree
    getDebtCeiling() returns (uint256) envfree
}

rule setDebtCeilingIntegrity(uint256 ceiling) {
    setDebtCeiling(ceiling);
    assert getDebtCeiling() == ceiling;
}
