// Source: contracts/7/specs/ReserveConfiguration.spec
// Literal property: rule setUnbackedMintCapIntegrity, lines 157-160
// Literal dependency source lines: 1;34-35;57;157-160
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
    setUnbackedMintCap(uint256) envfree
    getUnbackedMintCap() returns (uint256) envfree
}

rule setUnbackedMintCapIntegrity(uint256 unbackedMintCap) {
    setUnbackedMintCap(unbackedMintCap);
    assert getUnbackedMintCap() == unbackedMintCap;
}
