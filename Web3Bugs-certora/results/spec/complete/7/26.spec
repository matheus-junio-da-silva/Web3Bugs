// Source: contracts/7/specs/ReserveConfiguration.spec
// Literal property: rule setSupplyCapIntegrity, lines 139-142
// Literal dependency source lines: 1;28-29;57;139-142
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
    setSupplyCap(uint256) envfree
    getSupplyCap() returns (uint256) envfree
}

rule setSupplyCapIntegrity(uint256 supplyCap) {
    setSupplyCap(supplyCap);
    assert getSupplyCap() == supplyCap;
}
