// Original: contracts/12/specs/VariableDebtToken.spec:26-41; no additional CVL declarations
// Target: VariableDebtToken; historical POOL harness binding shown when used.
// CVL syntax preserved verbatim; CVL2 migration is outside catalog scope.
rule integirtyBalanceOfTotalSupply(address a, method f)
{
	env e;
	
	uint256 balanceABefore = balanceOf(e, a);
	uint256 totalSupplyBefore = totalSupply(e);
	 
	calldataarg arg;
	sinvoke f(e, arg); 
	require (f.selector != burn(address, uint256, uint256).selector  &&
		f.selector != mint(address, address, uint256, uint256).selector);
	uint256 balanceAAfter = balanceOf(e, a);
	uint256 totalSupplyAfter = totalSupply(e);

	assert  (balanceAAfter != balanceABefore  => ( balanceAAfter - balanceABefore  == totalSupplyAfter - totalSupplyBefore));
}
