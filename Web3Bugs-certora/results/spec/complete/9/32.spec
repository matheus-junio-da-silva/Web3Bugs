// Original: contracts/9/specs/governance.spec:62-74; property text copied without modification.
// Original CVL syntax preserved. Status: complete.
using Accounts as accounts

methods {
	getUpvoteRecord(address) returns uint256, uint256 envfree
}

definition upvoteInv(uint p, uint w) returns bool 
    = (p != 0 && w > 0) || (p == 0 && w == 0)
    ;

function callArbitrary(method f) {
	env e;
	calldataarg arg;
	f(e, arg);
}

rule upvotesConsistency(address u, method f) filtered { f -> !f.isView } {
    uint _p;
    uint _w;
    _p, _w = getUpvoteRecord(u);

    callArbitrary(f);

    uint p_;
    uint w_;
    p_, w_ = getUpvoteRecord(u);
    assert (_p == p_ && _w == w_) || upvoteInv(p_, w_);
    // the invariant is upvoteInv, defined here
} 
