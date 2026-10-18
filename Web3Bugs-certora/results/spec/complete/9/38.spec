// Original: contracts/9/specs/governance.spec:211-215; property text copied without modification.
// Original CVL syntax preserved. Status: complete.
using Accounts as accounts

methods {
	vote(uint256,uint256,uint8) returns bool
	proposalCount() returns uint256 envfree
	getFromDequeued(uint256) returns uint256 envfree
}

ghost votedFor(address,uint256) returns bool { // voter to proposal id voted for
    init_state axiom forall address v. forall address p. !votedFor(v, p);
}

hook Sstore voters[KEY address x].(offset 96)/*referendumVotes*/[KEY uint256 indx].(offset 32)/*proposal ID */ uint256 id STORAGE {
    require 0 <= x && x <= max_uint160;
    havoc votedFor assuming votedFor@new(x,id) == true
        && (forall address y. forall uint z. (y != x || z != id => votedFor@new(y,z) == votedFor@old(y,z)));
} 

invariant dequeuedIsWithinRange(uint i) getFromDequeued(i) <= proposalCount()

invariant referendumVoteIDIsLessThanOrEqCounter(address v, uint p) votedFor(v,p) => p <= proposalCount() {
    preserved vote(uint256 _, uint256 indx, uint8 vr) with (env e) {
        requireInvariant dequeuedIsWithinRange(indx); 
    }
}
