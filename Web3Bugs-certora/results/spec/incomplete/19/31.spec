// Origin OUSD historical CVL, extracted WITHOUT changing original rule/invariant text.
// Source: contracts/19/spec/ousdSum.spec lines 88-117; target: OUSDHarness

methods {
	balanceOf(address) returns uint256 envfree
}

definition summedFunction(address u) returns uint256 = balanceOf(u);

rule sum2Test(method f, address Addr1, address Addr2){
	env e;
	
	// Adderesses should be different
	require Addr1 != Addr2;
		
	// Balances before
	uint256 _r1Balance = summedFunction(Addr1);
	uint256 _r2Balance = summedFunction(Addr2);

	mathint _sumB = _r1Balance + _r2Balance;
	
	calldataarg arg;
	sinvoke f(e, arg);
	
	// Balances after
	uint256 r1Balance_ = summedFunction(Addr1);
	uint256 r2Balance_ = summedFunction(Addr2);
	
	mathint sumB_ = r1Balance_ + r2Balance_;
	
	bool c1 = (_r1Balance!=r1Balance_);
	bool c2 = (_r2Balance!=r2Balance_);
	
	// Function will check only the two addresses which balances were changed
	require c1 && c2;
	
	// after
	assert _r1Balance + _r2Balance == r1Balance_ + r2Balance_, "Violated: sum of two returns false.";
}	