// Original: contracts/9/specs/governance.spec:350-364; property text copied without modification.
// Original CVL syntax preserved. Status: complete.
using Accounts as accounts

function callArbitrary(method f) {
	env e;
	calldataarg arg;
	f(e, arg);
}

rule only_initializer_changes_initialized_field(method f) filtered { f -> !f.isView } {
	env _e;
	env eF;
	env e_;
	
	bool _isInitialized = initialized(_e);
		
	require f.selector != initialize(address,address,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256).selector;
	
    callArbitrary(f);
	
	bool isInitialized_ = sinvoke initialized(e_);
	
	assert _isInitialized == isInitialized_, "Method $f is not expected to change initialization field from ${_isInitialized} to ${isInitialized_}";
}
