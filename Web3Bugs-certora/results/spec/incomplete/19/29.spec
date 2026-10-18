// Origin OUSD historical CVL, extracted WITHOUT changing original rule/invariant text.
// Source: contracts/19/spec/ousdSum.spec lines 35-65; target: OUSDHarness

methods {
	balanceOf(address) returns uint256 envfree
}

definition summedFunction(address u) returns uint256 = balanceOf(u);

rule changesTwo(method f, address Addr1, address Addr2, address Addr3)
{
	env e;

	// Balances before
	uint256 _r1Balance = summedFunction(Addr1);
	uint256 _r2Balance = summedFunction(Addr2);
	uint256 _r3Balance = summedFunction(Addr3);
	
	// all the addresses should be different
	require !((Addr1 == Addr2) || ( Addr2 == Addr3) || ( Addr1 == Addr3) );
	
	calldataarg arg;
	sinvoke f(e, arg);
	
	// Balances after
	uint256 r1Balance_ = summedFunction(Addr1);
	uint256 r2Balance_ = summedFunction(Addr2);
	uint256 r3Balance_ = summedFunction(Addr3);	
	
	bool c1 = (_r1Balance!=r1Balance_);
	bool c2 = (_r2Balance!=r2Balance_);
	bool c3 = (_r3Balance!=r3Balance_);
	
	// helping variable
	bool changesAtLeastThree = ( (c1 && c2 && c3) );
	
	// If true, it changes <= 2
	assert !changesAtLeastThree, "Violated: changes less than or equal 2 violated.";
	
}
