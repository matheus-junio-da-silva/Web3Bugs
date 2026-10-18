// Original: contracts/12/specs/VariableDebtToken.spec:143-156; using declaration line 1
// Target: VariableDebtToken; historical POOL harness binding shown when used.
// CVL syntax preserved verbatim; CVL2 migration is outside catalog scope.
using LendingPoolHarnessForVariableDebtToken as POOL

rule additiveBurn(address a, uint256 x,  uint256 y) {
	env e;
	address asset;
	uint256 index = POOL.getReserveNormalizedVariableDebt(e, asset);
	storage initialStorage = lastStorage;
	sinvoke burn(e, a, x, index);
	sinvoke burn(e, a, y, index);
	uint256 balanceScenario1 = balanceOf(e, a);
	uint256 t = x + y;
	sinvoke burn(e, a, t ,index) at initialStorage;

	uint256 balanceScenario2 = balanceOf(e, a);
	assert balanceScenario1 == balanceScenario2, "burn is not additive";
}
