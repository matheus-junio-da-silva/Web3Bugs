// Original: contracts/9/specs/lockedGold.spec:128-150 — literal property body, preserved historical syntax.
// Dependency status: complete.
pragma specify 0.1

methods {
	getAccountNonvotingLockedGold(address)  returns uint256 envfree
	getTotalPendingWithdrawals(address) returns uint256 envfree
	getunlockingPeriod() returns uint256 envfree
	unlock(uint256) 
	pendingWithdrawalsNotFull(address) returns bool envfree
}


/**
 * Verifies that withdraws do not occur before the unlocking period has passed.
 */
rule noWithdrawBeforeUnlocking(address account, uint256 value, method f) {
	// We must make sure the length of pending withdrawals is not MAX_UINT, since then the `push` will make the length 0.
	// (this should have been checked by the solidity compiler)
	require(sinvoke pendingWithdrawalsNotFull(account), "Pending withdrawals are full");
	
	// Unlock a value and add it to pending withdrawals
	env _e;
	require(_e.msg.sender == account);
	sinvoke unlock(_e,value);

	// Try to run any function - adversary's goal is to succeed in unlocking before time
	env eF;
	require(eF.block.timestamp > _e.block.timestamp);
	calldataarg arg;
	sinvoke f(eF,arg);
	// We check if adversary succeeded
	uint256 totalPendingWithdrawals_ = sinvoke getTotalPendingWithdrawals(account);
	assert(
    eF.block.timestamp < _e.block.timestamp + sinvoke getunlockingPeriod() =>
    sinvoke getAccountNonvotingLockedGold(account) + totalPendingWithdrawals_ >= value,
    "If we are before the unlock period passed, we cannot transfer the value outside the locked balance or pending balance"
  );
}
