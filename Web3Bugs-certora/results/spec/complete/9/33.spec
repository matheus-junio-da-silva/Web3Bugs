// Original: contracts/9/specs/governance.spec:80-97; property text copied without modification.
// Original CVL syntax preserved. Status: complete.
using Accounts as accounts

methods {
	getUpvotes(uint256) returns uint256 envfree
	getUpvotedProposal(address) returns uint256 envfree
	getUpvoteRecord(address) returns uint256, uint256 envfree
  voteSignerToAccount(address) => DISPATCHER(true) UNRESOLVED
  accounts.voteSignerToAccount(address) returns (address) envfree
}

definition upvoteInv(uint p, uint w) returns bool 
    = (p != 0 && w > 0) || (p == 0 && w == 0)
    ;

rule no_double_upvote(uint256 p, address u) {
	uint256 _upvotes = getUpvotes(p);
	uint256 _usersUpvotedProposal = getUpvotedProposal(u);
	env e;
	require e.msg.sender == u && u != 0; // note that the sender is the signer here
    require accounts.voteSignerToAccount(u) == u;
	uint256 lesser; 
    uint256 greater;
	upvote(e, p, lesser, greater);
	uint256 upvotes_ = getUpvotes(p);
	
    uint voteRecordP;
    uint voteRecordW;
    voteRecordP, voteRecordW = getUpvoteRecord(u);
    require upvoteInv(voteRecordP, voteRecordW);
	assert _usersUpvotedProposal == p => upvotes_ <= _upvotes, 
		"Upvotes increased from ${_upvotes} to ${upvotes_} even though upvoted by user $u who already upvoted $p";
}
