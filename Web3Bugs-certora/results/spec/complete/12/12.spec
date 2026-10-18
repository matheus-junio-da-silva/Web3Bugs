// Original: contracts/12/specs/VariableDebtToken.spec:46-60; using declaration line 1
// Target: VariableDebtToken; historical POOL harness binding shown when used.
// CVL syntax preserved verbatim; CVL2 migration is outside catalog scope.
using LendingPoolHarnessForVariableDebtToken as POOL

rule integirtyBalanceOfTotalSupplyOnBurn(address a)
{
	env e;
	
	uint256 balanceABefore = balanceOf(e, a);
	uint256 totalSupplyBefore = totalSupply(e);
	 
	uint256 x;
	address asset;
	uint256 index = POOL.getReserveNormalizedVariableDebt(e, asset);
	sinvoke burn(e, a, x, index); 
	uint256 balanceAAfter = balanceOf(e, a);
	uint256 totalSupplyAfter = totalSupply(e);
	assert (balanceAAfter != balanceABefore  => (balanceAAfter - balanceABefore  == totalSupplyAfter - totalSupplyBefore));
}
