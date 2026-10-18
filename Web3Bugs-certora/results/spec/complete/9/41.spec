// Original: contracts/9/specs/governance.spec:271-287; property text copied without modification.
// Original CVL syntax preserved. Status: complete.
using Accounts as accounts

methods {
	getVoteTotals(uint256) returns uint256,uint256,uint256 envfree
}

rule execute_preconds(uint256 p, uint256 index) {
	// A proposal should never be executable when there are at least as many no votes as yes votes
	// TODO: A proposal should never be executable unless it received a yes:no vote ratio greater than that specified in the constitution
	env _e;
	env eF;
	
	uint256 _yes;
	uint256 _no;
	uint256 _abstain;
	_yes, _no, _abstain = getVoteTotals(p);
	
	bool executeRetval = execute@withrevert(eF,p,index);
	bool executeReverted = lastReverted;
	
	assert _no >= _yes => (!executeRetval || executeReverted), "If there are more no votes than yes votes, then we cannot succeed in executing";
	// TODO: may require to make sure that all constitutions demand at least majority
}
