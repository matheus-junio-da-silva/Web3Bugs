// Original: contracts/9/specs/governance.spec:244-268; property text copied without modification.
// Original CVL syntax preserved. Status: complete.
using Accounts as accounts

methods {
	isApproved(uint256) returns bool envfree
  proposalExists(uint256) returns bool
}

rule approved_proposals_invariants(method f, uint256 p) filtered { f -> !f.isView } {
	env _e;
	env eF;
	env e_;
	
	// Existence depends on timestamp, and we assume we are well past 0
	require e_.block.timestamp >= eF.block.timestamp 
			&& eF.block.timestamp >= _e.block.timestamp 
			&& _e.block.timestamp > 0;
			
	bool _doesProposalExist = proposalExists(_e,p);
	bool _isApprovedProposal = isApproved(p);
	
	require _isApprovedProposal => _doesProposalExist; // if a proposal is approved, it must be existent
	
	calldataarg arg;
	require !f.isView;
	sinvoke f(eF,arg);
	
	bool doesProposalExist_ = proposalExists(e_,p);
	bool isApprovedProposal_ = isApproved(p);
	
	assert isApprovedProposal_ => doesProposalExist_, "An approved proposal must exist";
	assert _isApprovedProposal => isApprovedProposal_ || !doesProposalExist_, "An approved proposal cannot be disapproved if it still exists";
}
