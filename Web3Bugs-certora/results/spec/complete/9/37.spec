// Original: contracts/9/specs/governance.spec:164-209; property text copied without modification.
// Original CVL syntax preserved. Status: complete.
using Accounts as accounts

methods {
	vote(uint256,uint256,uint8) returns bool
	proposalCount() returns uint256 envfree
	getNoneVoteEnum() returns uint256 envfree
	getAbstainVoteEnum() returns uint256 envfree
	getYesVoteEnum() returns uint256 envfree
	getNoVoteEnum() returns uint256 envfree
	getVoteTotals(uint256) returns uint256,uint256,uint256 envfree
	getVoteRecord(address,uint256) returns uint256, uint256, uint256 envfree
  proposalExists(uint256) returns bool
}

rule no_double_vote_referendum_all_but_vote(method f, address account, uint256 deqIndex) filtered { f -> !f.isView } {
	env eF; 
	env eFTime; // same time as eF;
	env e_;
	
	uint256 NONE_ENUM = getNoneVoteEnum();
	uint256 ABSTAIN = getAbstainVoteEnum();
	uint256 YES = getYesVoteEnum();
	uint256 NO = getNoVoteEnum();
	
	uint256 p; // a proposal - let's assume it already exists (required for propose() verification)
	uint256 recordValue;
	p, recordValue, _ = getVoteRecord(account,deqIndex);
	uint256 currentProposalCount = proposalCount();
	require currentProposalCount >= p;
	
	
	uint256 _yes; uint256 _no; uint256 _abstain;
	_yes,_no,_abstain = getVoteTotals(p);
	
	// if can't vote for NONE_ENUM, then necessarily if record vote is NONE_ENUM, all votes are zero currently
	require recordValue == NONE_ENUM => (_yes == 0 && _no == 0 && _abstain == 0);
	
	
	calldataarg arg;
	require f.selector != vote(uint256,uint256,uint8).selector;
    require f.selector != revokeVotes().selector;
	require !f.isView;
	require eF.msg.sender == account;
	f(eF,arg);
	
	uint256 yes_; uint256 no_; uint256 abstain_;
	yes_,no_,abstain_ = getVoteTotals(p);
	
	bool doesProposalExist_ = proposalExists(e_,p);
	
	// if p expires, then sum of votes is no longer relevant - happens in approve, vote, execute
	assert (recordValue != NONE_ENUM && doesProposalExist_) => (yes_ + no_ + abstain_) == (_yes + _no + _abstain), "Total votes could not have changed if already voted";
	assert recordValue == YES => yes_ <= _yes, "Yes votes could not have increased if voted yes already";
	assert recordValue == NO => no_ <= _no, "No votes could not have increased if voted no already";
	assert recordValue == ABSTAIN => abstain_ <= _abstain, "Abstain votes could not have increased if voted abstain already";
	assert recordValue == NONE_ENUM => (!doesProposalExist_ && yes_ == 0 && no_ == 0 && abstain_ == 0) // proposal no longer exists so everything is 0
									// or no votes changed
									|| (yes_ == _yes && no_ == _no && abstain_ == _abstain),
									"If previously did not vote, either this proposal was deleted, or no votes changed";
}
