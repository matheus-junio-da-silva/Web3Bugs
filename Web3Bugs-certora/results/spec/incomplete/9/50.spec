// Original: contracts/9/specs/governance_old_rules.spec:84-111; property text copied without modification.
// Original CVL syntax preserved. Status: incomplete.
rule constitution_change_legal(method f) filtered { f -> !f.isView } {
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
	// TODO: This needs to be re-written based on new library for fractions
	/*
	bool b1 = num_*2 <= denom_;
	bool b2 = num_ <= denom_;
	
	// if constitution is correct then we report that there was a change, but otherwise we report the incorrect change as well.
	// if constitution updated, check if it is correct. 
	assert changed => b1, "Updated constitution: Constitution must be at least majority, but got less: ${num_} to ${denom_}";
	assert changed => b2, "Updated constitution: Constitution cannot demand more than unanimous, but got ${num_} to ${denom_}";
	*/
	assert true;
}
