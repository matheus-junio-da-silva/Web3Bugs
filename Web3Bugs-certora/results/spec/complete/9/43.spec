// Original: contracts/9/specs/governance.spec:311-323; property text copied without modification.
// Original CVL syntax preserved. Status: complete.
using Accounts as accounts

methods {
    getQueueLength() returns uint256 envfree
}

function callArbitrary(method f) {
	env e;
	calldataarg arg;
	f(e, arg);
}

rule can_add_to_queue(method f) filtered { f -> 
    !f.isView
    && f.selector != propose(uint256[],address[],bytes,uint256[],string).selector
} {
	uint256 _queueLength = getQueueLength();
	
	callArbitrary(f);
	
	uint256 queueLength_ = getQueueLength();
	
	assert queueLength_ <= _queueLength, 
		"Method can queue elements - should check separately that cannot queue proposal IDs equal 0 (proposal_count_monotonic_increasing)";
}
