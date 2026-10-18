// Original: contracts/12/specs/VariableDebtToken.spec:164-174; using declaration line 1
// Target: VariableDebtToken; historical POOL harness binding shown when used.
// CVL syntax preserved verbatim; CVL2 migration is outside catalog scope.
using LendingPoolHarnessForVariableDebtToken as POOL

rule inverseMintBurn(address a, uint256 x) {
	env e;
	address asset;
	address delegatedUser;
	uint256 index = POOL.getReserveNormalizedVariableDebt(e, asset);
	uint256 balancebefore = balanceOf(e, a);
	sinvoke mint(e, delegatedUser, a, x, index);
	sinvoke burn(e, a, x, index);
	uint256 balanceAfter = balanceOf(e, a);
	assert balancebefore == balanceAfter, "burn is not the inverse of mint";
}
