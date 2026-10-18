// Source: contracts/7/specs/ReserveConfiguration.spec
// Literal property: rule setDecimalsIntegrity, lines 79-82
// Literal dependency source lines: 1;8-9;57;79-82
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
    setDecimals(uint256) envfree
    getDecimals() returns (uint256) envfree
}

rule setDecimalsIntegrity(uint256 decimals) {
    setDecimals(decimals);
    assert getDecimals() == decimals;
}
