// Original: contracts/9/specs/lockedGold.spec:80-107 — literal property body, preserved historical syntax.
// Dependency status: complete.
pragma specify 0.1

methods {
	getAccountNonvotingLockedGold(address)  returns uint256 envfree
	ercBalanceOf(address) returns uint256 envfree
	getTotalPendingWithdrawals(address) returns uint256 envfree
	getPendingWithdrawalsLength(address) returns uint256 envfree
	incrementNonvotingAccountBalance(address, uint256) 
	decrementNonvotingAccountBalance(address, uint256) 
	getGoldTokenExt() returns address envfree
}


/**
 * An address' total gold cannot be changed by any other contract's function calls.
 */
rule noChangeByOther(address a, address b, method f) {
	require(a != b);
	// We assume the sender is not the currentContract
	require(
    a != currentContract &&
    (a == sinvoke getGoldTokenExt() => f.selector != withdraw(uint256).selector));
	uint256 _ercBalance = sinvoke ercBalanceOf(a);
	uint256 _accountNonVoting = sinvoke getAccountNonvotingLockedGold(a);
	uint256 _accountTotalPendingWithdrawals =  sinvoke getTotalPendingWithdrawals(a);
	// We limit the amount of pending records due to loop handling 
	uint length = sinvoke getPendingWithdrawalsLength(a);
	require(length <= 1);
	env eF;
	require(eF.msg.sender == b);
	calldataarg arg;
	require(
    f.selector != decrementNonvotingAccountBalance(address,uint256).selector &&
    f.selector != incrementNonvotingAccountBalance(address,uint256).selector &&
    f.selector != slash(address,uint256,address,uint256,address[],address[],uint256[]).selector
  );
	sinvoke f(eF,arg);
	uint256 ercBalance_ = sinvoke ercBalanceOf(a); 
	uint256 accountNonVoting_ = sinvoke getAccountNonvotingLockedGold(a);
	uint256 accountTotalPendingWithdrawals_ =  sinvoke getTotalPendingWithdrawals(a);
	assert(f.selector != withdraw(uint256).selector => _ercBalance == ercBalance_, "Unexpected change to erc tokens");
	assert(_accountTotalPendingWithdrawals == accountTotalPendingWithdrawals_, "Unexpected change to total pending");
	assert(_accountNonVoting == accountNonVoting_, "Unexpected change to account nonvoting");
}
