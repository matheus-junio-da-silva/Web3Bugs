// Original: contracts/9/specs/governance_old_rules.spec:4-55; property text copied without modification.
// Original CVL syntax preserved. Status: incomplete.
rule no_double_vote_referendum_vote(address account, uint256 deqIndex) {
	/* A user that already has a vote record for a dequeued index, cannot make a transaction that will increase the weight of that choice */
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
	
	require accounts.voteSignerToAccount(eF.msg.sender) == account;
	uint256 someP; uint256 someIndex; uint8 someValue;
	
	uint256 pOfSomeIndex;
	pOfSomeIndex, _, _ = getVoteRecord(account,someIndex);
	require pOfSomeIndex == p => someIndex == deqIndex; // no duplicates in the dequeued array
	require someP == p => someIndex == deqIndex;
	
	vote(eF,someP,someIndex,someValue);
	
	
	uint256 yes_; uint256 no_; uint256 abstain_;
	yes_,no_,abstain_ = getVoteTotals(p);
	
	bool doesProposalExist_ = proposalExists(e_,p);
	
	// if p expires, then sum of votes is no longer relevant - happens in approve, vote, execute
	assert (recordValue != NONE_ENUM && doesProposalExist_) => (yes_ + no_ + abstain_) == (_yes + _no + _abstain), "Total votes could not have changed if already voted";
	assert recordValue == YES => yes_ <= _yes, "Yes votes could not have increased if voted yes already";
	assert recordValue == NO => no_ <= _no, "No votes could not have increased if voted no already";
	assert recordValue == ABSTAIN => abstain_ <= _abstain, "Abstain votes could not have increased if voted abstain already";
	assert recordValue == NONE_ENUM => (!doesProposalExist_ && yes_ == 0 && no_ == 0 && abstain_ == 0)// proposal no longer exists so everything is 0
									// or just one out of (yes,no,abstain) changed
									|| (yes_ == _yes && no_ == _no)
									|| (yes_ == _yes && abstain_ == _abstain)
									|| (no_ == _no && abstain_ == _abstain),
									"If previously did not vote, either this proposal was deleted, or only one kind of vote may change, and the other two are the same";
}
