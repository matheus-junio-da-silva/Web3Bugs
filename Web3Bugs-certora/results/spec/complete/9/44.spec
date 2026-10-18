// Original: contracts/9/specs/governance.spec:325-347; property text copied without modification.
// Original CVL syntax preserved. Status: complete.
using Accounts as accounts

function callArbitrary(method f) {
	env e;
	calldataarg arg;
	f(e, arg);
}

rule constitution_change(method f) filtered { f -> 
    !f.isView
        && f.selector != setConstitution(address,bytes4,uint256).selector
} {
	env _e;
	env eF;
	env e_;
	
	calldataarg arg_getConstitution;
	
	uint256 _res;
	_res = getConstitution(_e,arg_getConstitution);
	
    callArbitrary(f);
	
	uint256 res_;
	res_ = getConstitution(e_,arg_getConstitution);
	
	bool changed = !(_res == res_);
	
	// we're going to demand hard equality here - so 1/2 and 2/4 are INEQUAL
	assert !changed, "changes constitution";
}
