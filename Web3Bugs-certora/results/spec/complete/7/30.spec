// Source: contracts/7/specs/ReserveConfiguration.spec
// Literal property: rule setEModeCategoryIntegrity, lines 163-166
// Literal dependency source lines: 1;36-37;57;163-166
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
    setEModeCategory(uint256) envfree
    getEModeCategory() returns (uint256) envfree
}

rule setEModeCategoryIntegrity(uint256 category) {
    setEModeCategory(category);
    assert getEModeCategory() == category;
}
