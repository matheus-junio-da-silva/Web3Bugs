// Original: contracts/12/specs/VariableDebtToken.spec:129-138; using declaration line 1
// Target: VariableDebtToken; historical POOL harness binding shown when used.
// CVL syntax preserved verbatim; CVL2 migration is outside catalog scope.
using LendingPoolHarnessForVariableDebtToken as POOL

rule integrityBurn(address a, uint256 x) {
	env e;
	address asset;
	uint256 index = POOL.getReserveNormalizedVariableDebt(e, asset);
	uint256 balancebefore = balanceOf(e, a);
	sinvoke burn(e, a, x, index);
	
	uint256 balanceAfter = balanceOf(e, a);
	assert balanceAfter == balancebefore - x;
}
