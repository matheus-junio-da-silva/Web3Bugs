// Original: contracts/9/specs/lockedGold.spec:151-169 — literal property body, preserved historical syntax.
// Dependency status: complete.
pragma specify 0.1


/**
 * Verifies initialization value does not change.
 */
rule only_initializer_changes_initialized_field(method f) {
	env _e;
	env eF;
	env e_;

	bool _isInitialized = sinvoke initialized(_e);
	require(f.selector != initialize(address,uint256).selector);
	calldataarg arg;
	invoke f(eF,arg);
	bool isInitialized_ = sinvoke initialized(e_);
	assert(
    _isInitialized == isInitialized_,
    "Method $f is not expected to change initialization field from ${_isInitialized} to ${isInitialized_}"
  );
}
