// Original: contracts/9/specs/lockedGold.spec:42-75 — literal property body, preserved historical syntax.
// Dependency status: complete.
pragma specify 0.1

methods {
	getAccountNonvotingLockedGold(address)  returns uint256 envfree
	ercBalanceOf(address) returns uint256 envfree
	getTotalPendingWithdrawals(address) returns uint256 envfree
	getPendingWithdrawalsLength(address) returns uint256 envfree
	incrementNonvotingAccountBalance(address, uint256) 
	decrementNonvotingAccountBalance(address, uint256) 
}


/**
 * Total here refers to the sum of address balance and locked gold (voting and nonvoting). 
 */
rule totalPreserved(address account, method f) {
	// We assume the sender is not the currentContract
	require(account != currentContract);
	uint256 _ercBalance = sinvoke ercBalanceOf(account); 
	uint256 _accountNonVoting = sinvoke getAccountNonvotingLockedGold(account);
	uint256 _accountTotalPendingWithdrawals =  sinvoke getTotalPendingWithdrawals(account);
	// We limit the amount of pending records due to loop handling 
	require sinvoke getPendingWithdrawalsLength(account) <= 1;
	env eF;
	require(eF.msg.sender == account);
	// These three function are exceptions to the rule (they are designed to affect total)
	require(
    f.selector != decrementNonvotingAccountBalance(address,uint256).selector &&
    f.selector != incrementNonvotingAccountBalance(address,uint256).selector &&
    f.selector != slash(address,uint256,address,uint256,address[],address[],uint256[]).selector
  );
	calldataarg arg;
	sinvoke f(eF,arg);
	// We limit the amount of pending records due to loop handling 
	uint length = sinvoke getPendingWithdrawalsLength(account);
	require(length <= 1);
	uint256 ercBalance_ = sinvoke ercBalanceOf(account);
	uint256 accountNonVoting_ = sinvoke getAccountNonvotingLockedGold(account);
	uint256 accountTotalPendingWithdrawals_ =  sinvoke getTotalPendingWithdrawals(account);
  assert(
    _ercBalance + _accountNonVoting + _accountTotalPendingWithdrawals ==
    ercBalance_ + accountNonVoting_ + accountTotalPendingWithdrawals_,
    "Total of tokens not preserved"
  );
}
