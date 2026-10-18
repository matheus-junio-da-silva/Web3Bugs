// Source: contracts/7/specs/pool.spec
// Literal property: rule getReserveNormalizedVariableDebtCheck, lines 197-209
// Literal dependency source lines: 9;21;56;104;197-209
// Historical syntax retained; no reconstruction or CVL2 migration.

using ATokenHarness as _aToken

methods {
    getCurrScaledVariableDebt(address) returns (uint256) envfree
}

rule getReserveNormalizedVariableDebtCheck()
{
	env e1;
	calldataarg args;
	calldataarg args2;
    address asset; uint256 amount; address onBehalfOf; uint16 referralCode;
    require asset != _aToken;
	uint256 oldIndex = getReserveNormalizedVariableDebt(e1, args);
    uint256 totalDebtBefore = getCurrScaledVariableDebt(asset);
	supply(e1, asset, amount, onBehalfOf, referralCode);
	uint256 newIndex = getReserveNormalizedVariableDebt(e1, args);
	assert totalDebtBefore != 0 => newIndex >= oldIndex;
}
