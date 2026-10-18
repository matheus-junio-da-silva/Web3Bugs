// Original: contracts/9/specs/goverance_with_dequeue.spec:19-49; property text copied without modification.
// Original CVL syntax preserved. Status: complete.
rule promote_proposal(method f, uint256 p, uint256 index) filtered { f -> !f.isView } {
	/* A proposal should never be able to be promoted from the queue if it was proposed more than queueExpiry seconds ago */
	// Let's say we have an empty index. Then it cannot be filled with a new proposal p if its submit time is more than queueExpiry seconds ago
	env eF;
	
	// p must be non zero
	require p != 0;
	
	// get queue expiry
	uint256 _queueExpiry = queueExpiry();
	
	// require index to be valid and to be empty
	require index >= 0;
	uint256 queueLength = getDequeuedLength();
	require index <= queueLength || index == queueLength+1; // either an empty index or the next one we push
	// if it's an empty index in the range, then it's empty
	require index <= queueLength => getFromDequeued(index) == 0;
	
	// fetch proposal p timestamp
	uint256 _proposalTimestamp;
	_,_, _proposalTimestamp, _ = getProposalSlim(p);
	
	// invoke f
	calldataarg arg;
	require !f.isView;
	sinvoke f(eF,arg);

	// deqeued index should contain p now only if eF.block.timestamp is not past p's timestamp+queueExpiry
	assert getFromDequeued(index) == p => eF.block.timestamp <= _proposalTimestamp + _queueExpiry, 
		"Managed to promote $p in ${eF.block.timestamp} after proposal timestamp ${_proposalTimestamp} + ${_queueExpiry}";
}
