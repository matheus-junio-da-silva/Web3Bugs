// Original: contracts/9/specs/governance.spec:218-241; property text copied without modification.
// Original CVL syntax preserved. Status: complete.
using Accounts as accounts

methods {
	getFromDequeued(uint256) returns uint256 envfree
	isApproved(uint256) returns bool envfree
	isDequeuedProposalExpired(uint256) returns bool
	approver() returns address envfree
}

rule approval_only_if_promoted_and_allowed(uint256 p, uint256 index) {
	// A proposal should never be able to be approved unless it was promoted from the queue
	env eF;
    env eGet;
    require eF.block.timestamp == eGet.block.timestamp;
    require eF.block.number == eGet.block.number;
	
	bool _isProposalApproved = isApproved(p);
	bool _isDequeued = getFromDequeued(index) == p;
	bool _isExpired = isDequeuedProposalExpired(eGet, p);
	
	address _approver = approver();
	require !_isProposalApproved; // we assume not approved yet
	require !_isExpired; // we also assume it did not expire
		
	approve(eF,p,index);
	// should check if dequeued right during approve
	bool isDequeued_ = getFromDequeued(index) == p;
	
	bool isProposalApproved_ = isApproved(p);
	
	assert isProposalApproved_ => _isDequeued || (!_isDequeued && isDequeued_), "Cannot approve proposal $p unless $index points to it before approve or during it"; // index has p
	assert isProposalApproved_ => eF.msg.sender == _approver, "Only approver ${_approver} can approve";
}
