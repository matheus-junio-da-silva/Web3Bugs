// Origin OUSD historical CVL, extracted WITHOUT changing original rule/invariant text.
// Source: contracts/19/spec/ousdSum.spec lines 7-33; target: OUSDHarness

methods {
	balanceOf(address) returns uint256 envfree
}

definition summedFunction(address u) returns uint256 = balanceOf(u);

rule changesOne(method f, address Addr1, address Addr2)
{
	env e;
	
	// Balances before
	uint256 _r1Balance = summedFunction(Addr1);
	uint256 _r2Balance = summedFunction(Addr2);
	
	require !(Addr1 == Addr2);
	
	calldataarg arg;
	sinvoke f(e, arg);
	
	// Balances after
	uint256 r1Balance_ = summedFunction(Addr1);
	uint256 r2Balance_ = summedFunction(Addr2);
		
	bool c1 = (_r1Balance!=r1Balance_);
	bool c2 = (_r2Balance!=r2Balance_);
	
	// helping variable
	bool changesAtLeastTwo = ( (c1 && c2) );
	
	// If true, it changes <= 1
	assert !changesAtLeastTwo, "Violated: changes less than or equal 1 violated.";

}
