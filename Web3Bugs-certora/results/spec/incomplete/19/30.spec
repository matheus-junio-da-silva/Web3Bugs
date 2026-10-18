// Origin OUSD historical CVL, extracted WITHOUT changing original rule/invariant text.
// Source: contracts/19/spec/ousdSum.spec lines 67-86; target: OUSDHarness

methods {
	balanceOf(address) returns uint256 envfree
}

definition summedFunction(address u) returns uint256 = balanceOf(u);

rule sum1Test(method f, address Addr1){
	env e;
	
	// Balances before
	uint256 _r1Balance = summedFunction(Addr1);
	
	calldataarg arg;
	sinvoke f(e, arg);
	
	// Balances after
	uint256 r1Balance_ = summedFunction(Addr1);
	
	bool c1 = (_r1Balance!=r1Balance_);
	
	// Function will check only the address which balance was changed
	require c1;
	
	// after
	assert _r1Balance == r1Balance_, "Violated: sum of one returns false.";
}
