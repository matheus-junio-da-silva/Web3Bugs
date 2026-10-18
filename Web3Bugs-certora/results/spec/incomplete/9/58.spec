// Original: contracts/9/specs/locked_gold_linked.spec:4-19 — literal property body, preserved historical syntax.
// Dependency status: incomplete.
/**
 * Validators can not delegate validation while registered as validators.
 */
rule no_validate_delegation_when_validating {
	env _e;
	env eF;
	
	address account = eF.msg.sender;
	bool _isAccountValidating = sinvoke _isValidating(_e,account);

	calldataarg arg;
	invoke delegateValidating(eF,arg);
	bool succeededDelegate = !lastReverted;
	
	assert(
    _isAccountValidating => !succeededDelegate,
    "Account successfully delegated validating even though it is already a validator"
  );
} 
