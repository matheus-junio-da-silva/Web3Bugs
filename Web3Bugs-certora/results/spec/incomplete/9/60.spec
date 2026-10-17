// Original: contracts/9/specs/locked_gold_linked.spec:40-61 — literal property body, preserved historical syntax.
// Dependency status: incomplete.

/**
 * Accounts can not change account weight while already voting.
 */
rule no_weight_changing_when_voting(method f, address account) {
	env _e;
	uint256 _accountWeight = sinvoke _weight(_e,account);
	
	bool isAccountVoting = sinvoke isVoting(_e,account);
	
	env eF;
	calldataarg arg;
	invoke f(eF,arg);
	
	env e_;
	uint256 accountWeight_ = sinvoke _weight(e_,account);
	
	assert(
    isAccountVoting => _accountWeight == accountWeight_,
    "Method changed weight of account if voting"
  );
}
