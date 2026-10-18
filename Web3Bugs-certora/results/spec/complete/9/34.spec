// Original: contracts/9/specs/governance.spec:99-114; property text copied without modification.
// Original CVL syntax preserved. Status: complete.
using Accounts as accounts

methods {
	proposalCount() returns uint256 envfree
}

function callArbitrary(method f) {
	env e;
	calldataarg arg;
	f(e, arg);
}

rule proposal_count_monotonic_increasing(method f) filtered { f -> !f.isView } {
	// proposal count is monotonic increasing (strictly in propose)
		
	uint256 _count = proposalCount();
	
    callArbitrary(f);

	uint256 count_ = proposalCount();
	
	if (f.selector == propose(uint256[],address[],bytes,uint256[],string).selector && !f.isFallback) {
		assert count_ > _count, "Successful propose must increase proposal count";
		assert count_ > 0, "Proposal cannot be 0"; // this is already obvious - even one proposal will increase count to 1
	}

	assert count_ >= _count, "Proposal count must not decrease";
}
