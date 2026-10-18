// Project 13: original historical CVL, Example 51
// Original source: certora/governance/GovernanceAction.spec:19-31
// Included original CVL ranges: certora/governance/GovernanceAction.spec:10-10;12-12;16-17;19-31
// CVL2 conversion intentionally out of scope

methods {
getDepositParameters(uint16 currencyId) returns (int256[], int256[]) envfree
getMaxMarketIndex(uint16 currencyId) returns (uint256) envfree
}

definition MAX_MARKET_INDEX() returns uint256 = 7;

rule updateDepositParametersSetsProperly(
    uint16 currencyId,
    uint32[] _depositShares,
    uint32[] _leverageThresholds
) {
    env e;
    require getMaxMarketIndex() <= MAX_MARKET_INDEX();
    require _depositShares.length == getMaxMarketIndex();
    require _depositShares.length == _leverageThresholds.length;
    updateDepositParameters(currencyId, _depositShares, _leverageThresholds);
    // TODO: move the checking into solidity and return a bool on success.
    int256[] depositShares, int256[] leverageThresholds = getDepositParameters(currencyId)
}
