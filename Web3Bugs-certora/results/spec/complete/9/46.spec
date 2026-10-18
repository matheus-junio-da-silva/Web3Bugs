// Original: contracts/9/specs/governance.spec:366-381; property text copied without modification.
// Original CVL syntax preserved. Status: complete.
using Accounts as accounts

rule check_initializer {
	env _e;
	env eF;
	env e_;
	
	bool _isInitialized = initialized(_e);
	
	calldataarg arg;
	initialize@withrevert(eF,arg);
	bool successInit = !lastReverted;
	
	bool isInitialized_ = initialized(e_);
	
	assert _isInitialized => !successInit, "initialize() must revert if already initialized";
	assert successInit => isInitialized_, "When initialize() succeeds, must set initialization field to true";
}
