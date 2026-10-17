// Original: contracts/9/specs/locked_gold_linked.spec:20-39 — literal property body, preserved historical syntax.
// Dependency status: incomplete.

/**
 * Accounts can not delegate votes if already voting.
 */
rule no_vote_delegation_when_voting {
	env _e;
	env eF;
	
	address account = eF.msg.sender;
	bool _isAccountVoting = sinvoke isVoting(_e,account);

	calldataarg arg;
	invoke delegateVoting(eF,arg);
	bool succeededDelegate = !lastReverted;
	
	assert(
    _isAccountVoting => !succeededDelegate,
    "Account successfully delegated voting even though it is already a voter"
  );
} 
