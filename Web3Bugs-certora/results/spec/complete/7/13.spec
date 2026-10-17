// Source: contracts/7/specs/ReserveConfiguration.spec
// Literal property: rule setLtvIntegrity, lines 61-64
// Literal dependency source lines: 1-3;57;61-64
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
    setLtv(uint256) envfree
    getLtv() returns (uint256) envfree
}

rule setLtvIntegrity(uint256 ltv) {
    setLtv(ltv);
    assert getLtv() == ltv;
}
