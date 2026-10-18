// Original: contracts/9/specs/lockedGold.spec:112-123 — literal property body, preserved historical syntax.
// Dependency status: complete.
pragma specify 0.1

methods {
	ercBalanceOf(address) returns uint256 envfree
	getPendingWithdrawalsIndex(address,uint256) returns uint256 envfree	
}


/**
 * This rule verifies the Certora Prover is correctly modeling the behavior of GoldToken._transfer.
 */
rule withdraw(uint256 index) {
	env e;
	uint256 _balance = sinvoke ercBalanceOf(e.msg.sender);
	uint256 val = sinvoke getPendingWithdrawalsIndex(e.msg.sender, index);
	sinvoke withdraw(e, index);
	require (e.msg.sender != currentContract);
	uint256 balance_ = sinvoke ercBalanceOf(e.msg.sender);
	assert(
    _balance + val == balance_,
    "Withdraw balance not updated"
  );
}
