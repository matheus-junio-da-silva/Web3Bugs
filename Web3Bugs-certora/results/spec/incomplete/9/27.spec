// Original: contracts/9/specs/goverance_with_dequeue.spec:2-17; property text copied without modification.
// Original CVL syntax preserved. Status: incomplete.
rule may_dequeue(method f, uint256 index) filtered { f -> !f.isView } {
	// a utility rule for figuring out which methods could dequeue and whether it's all due to dequeueProposalsIfReady calls.

	// require index to be valid and to be empty
	require index >= 0;
	uint256 queueLength = getDequeuedLength();
	require index <= queueLength || index == queueLength+1; // either an empty index or the next one we push
	// if it's an empty index in the range, then it's empty
	require index <= queueLength => getFromDequeued(index) == 0;
	
	callArbitrary(f);
	
	uint256 newValueInDequeued = getFromDequeued(index);
	
	assert newValueInDequeued == 0, "Method caused a dequeue of proposal $newValueInDequeued to index $index";	
}
