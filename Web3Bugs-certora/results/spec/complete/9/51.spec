// Original: contracts/9/specs/lockedGold.spec:23-41 — literal property body, preserved historical syntax.
// Dependency status: complete.
pragma specify 0.1

methods {
	getNonvotingLockedGold() returns uint256 envfree	
	getAccountNonvotingLockedGold(address)  returns uint256 envfree
	incrementNonvotingAccountBalance(address, uint256) 
	decrementNonvotingAccountBalance(address, uint256) 
	unlock(uint256) 
}


/**
 * Account's nonvoting gold cannot exceed total locked nonvoting gold.
 */
rule totalNonVotingGEAccountNonVoting(address a, method f) {
	require(sinvoke getNonvotingLockedGold()  >= sinvoke getAccountNonvotingLockedGold(a));
	require(
    f.selector != decrementNonvotingAccountBalance(address,uint256).selector &&
    f.selector != incrementNonvotingAccountBalance(address,uint256).selector
  );
	env eF; 
	require(
    (f.selector != unlock(uint256).selector || eF.msg.sender == a) &&
    f.selector != slash(address,uint256,address,uint256,address[],address[],uint256[]).selector
  );
	calldataarg arg;
	sinvoke f(eF,arg);
	assert(sinvoke getNonvotingLockedGold() >= sinvoke getAccountNonvotingLockedGold(a));
}
