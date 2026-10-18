// Original: contracts/9/specs/governance.spec:118-141; property text copied without modification.
// Original CVL syntax preserved. Status: complete.
using Accounts as accounts

methods {
	isApproved(uint256) returns bool envfree
	getVoteTotals(uint256) returns uint256,uint256,uint256 envfree
}

function callArbitrary(method f) {
	env e;
	calldataarg arg;
	f(e, arg);
}

rule no_referendum_votes_unless_approved(method f, uint256 p) filtered { f -> !f.isView } {
	// A proposal should never be able to receive a vote unless it was approved
	env eF;
	
	uint256 _yes;
	uint256 _no;
	uint256 _abstain;
	_yes, _no, _abstain = getVoteTotals(p);
	
	// no votes currently
	require _yes == 0 && _no == 0 && _abstain == 0;
	
	bool _isProposalApproved = isApproved(p);
	
	callArbitrary(f);
	
	uint256 yes_;
	uint256 no_;
	uint256 abstain_;
	yes_, no_, abstain_ = getVoteTotals(p);
	
	assert (yes_ != 0 || no_ != 0 || abstain_ != 0) => _isProposalApproved, 
		"Cannot move from 0 votes to positive number of yes,no,abstain votes unless proposal $p is approved.";
}
