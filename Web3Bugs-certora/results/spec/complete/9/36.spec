// Original: contracts/9/specs/governance.spec:143-161; property text copied without modification.
// Original CVL syntax preserved. Status: complete.
using Accounts as accounts

methods {
	vote(uint256,uint256,uint8) returns bool
	getNoneVoteEnum() returns uint256 envfree
	getVoteRecord(address,uint256) returns uint256, uint256, uint256 envfree
  getVoteSigner(address) returns address => DISPATCHER(true) UNRESOLVED
  accounts.getVoteSigner(address) returns (address) envfree
}

rule cant_unvote(uint256 deqIndex, uint8 voteValue) {	
    env eF;
	uint256 NONE_ENUM = getNoneVoteEnum();
	// get the voting delegate
	address voterDelegate = accounts.getVoteSigner(eF.msg.sender);
	
	// check if voted
    uint256 p;
	uint256 recordValue;
    uint256 weight;
	p, recordValue, weight = getVoteRecord(voterDelegate,deqIndex);
	bool result = vote(eF,p,deqIndex,voteValue);
	
	uint256 recordValue_;
    uint256 weight_;
	_, recordValue_, weight_ = getVoteRecord(voterDelegate,deqIndex);
	
	assert voteValue == NONE_ENUM => (!result && recordValue_ == recordValue && weight_ == weight), "Cannot vote for none: function either returns false and did not update the vote, or it reverted"; // not voting none. reverting is fine and is encoded by the safe invoke
}
