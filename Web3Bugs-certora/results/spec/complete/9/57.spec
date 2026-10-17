// Original: contracts/9/specs/lockedGold.spec:170-194 — literal property body, preserved historical syntax.
// Dependency status: complete.
pragma specify 0.1


/**
 * Verifies `initialize` behaves correctly:
 * Reverts if already initialized,
 * Sets initialized to true if not.
 */
rule check_initializer {
	env _e;
	env eF;
	env e_;
	
	bool _isInitialized = sinvoke initialized(_e);
	calldataarg arg;
	invoke initialize(eF,arg);
	bool successInit = !lastReverted;
	bool isInitialized_ = sinvoke initialized(e_);
	assert(
    _isInitialized => !successInit,
    "Initialize() must revert if already initialized"
  );
	assert(
    successInit => isInitialized_,
    "When initialize() succeeds, must set initialization field to true"
  );
}
