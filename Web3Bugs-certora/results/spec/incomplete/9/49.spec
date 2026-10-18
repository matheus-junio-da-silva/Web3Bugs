// Original: contracts/9/specs/governance_old_rules.spec:60-81; property text copied without modification.
// Original CVL syntax preserved. Status: incomplete.
rule sum_of_votes_cannot_exceed_total_weight(method f, uint256 p) filtered { f -> !f.isView } {
	uint256 _totalWeight = getTotalLockedGold();
	// TODO: Must make sure that governance is not capable of invoking any function that changes the state of BondedDeposits and specifically totalWeight
	
	uint256 _yes;
	uint256 _no;
	uint256 _abstain;
	_yes, _no, _abstain = getVoteTotals(p);
	
	require _yes+_no+_abstain <= _totalWeight;
	
    callArbitrary(f);
	
	uint256 totalWeight_ = getTotalLockedGold();
	
	uint256 yes_;
	uint256 no_;
	uint256 abstain_;
	yes_, no_, abstain_ = getVoteTotals(p);
	
	assert yes_+no_+abstain_ <= totalWeight_, "Sum of votes for a proposal cannot exceed total weight";
}
