// Original: contracts/9/specs/goverance_with_dequeue.spec:55-74; property text copied without modification.
// Original CVL syntax preserved. Status: complete.
rule no_promoting_without_upvotes(uint256 p, uint256 index) {
	// Can a proposal be promoted with 0 votes? 
	env _e;
	env eF;
	env e_;
	
	/* would actually want forall index. inrange(index) => dequeued[index] != p but here its suffice to 'pre-guess' the index of the proposal we dequeue */
	// require index to be valid and to be empty
	require index >= 0;
	require p > 0; // proposal 0 is not legal, and cannot happen (we check it)
	uint256 queueLength = getDequeuedLength();
	require index <= queueLength || index == queueLength+1; // either an empty index or the next one we push
	// if it's an empty index in the range, then it's empty
	require index <= queueLength => getFromDequeued(index) == 0;
	
	uint256 _upvotes = getUpvotes(p);
	
	dequeueProposalsIfReady(eF);
	assert getFromDequeued(index) == p => _upvotes > 0, "Cannot dequeue (promote) proposal $p to index $index unless had some upvotes";
}
