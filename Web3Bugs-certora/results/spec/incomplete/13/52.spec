// Project 13: original historical CVL, Example 52
// Original source: certora/governance/GovernanceAction.spec:35-45
// Included original CVL ranges: certora/governance/GovernanceAction.spec:11-11;13-13;35-45
// CVL2 conversion intentionally out of scope

methods {
nTokenAddress(uint16 currencyId) returns (address) envfree
getNTokenAccount(address tokenAddress) returns (bytes6, uint256) envfree
}


rule updateIncentiveEmissionRateSetsProperly(
    uint16 currencyId,
    uint32 newEmissionRate,
    address nTokenAddress
) {
    env e;
    require nTokenAddress(currencyId) == nTokenAddress;
    updateIncentiveEmissionRate(currencyId, newEmissionRate);
    _, uint256 incentiveEmissionRate = getNTokenAccount(nTokenAddress);
    assert incentiveEmissionRate == newEmissionRate;
}
