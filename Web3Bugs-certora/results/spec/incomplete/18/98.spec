// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC721Votes.spec lines 201-217
// Target: ERC721Votes (historical voting harness)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC721Votes.spec:6-12
methods {
    numCheckpoints(address) returns (uint32) envfree
    getVotes(address) returns (uint256) envfree
    delegates(address) returns (address) envfree
    _delegate(address, address)
}

// Original CVL declaration: ERC721Votes.spec:44-50
hook Sstore _checkpoints[KEY address account].votes uint224 newVotes (uint224 oldVotes) STORAGE {
    havoc userVotes assuming
        userVotes@new(account) == newVotes;

    havoc totalVotes assuming
        totalVotes@new() == totalVotes@old() + to_mathint(newVotes) - to_mathint(userVotes(account));
}

// Original CVL declaration: ERC721Votes.spec:62-68
hook Sstore _checkpoints[KEY address account].fromBlock uint32 newBlock (uint32 oldBlock) STORAGE {
    havoc lastFromBlock assuming
        lastFromBlock@new(account) == newBlock;
    
    havoc doubleFromBlock assuming 
        doubleFromBlock@new(account) == (newBlock == lastFromBlock(account));
}

// Original CVL declaration: ERC721Votes.spec:34-36
ghost userVotes(address) returns uint224{
        init_state axiom forall address a. userVotes(a) == 0;
}

// Original CVL declaration: ERC721Votes.spec:39-42
ghost totalVotes() returns mathint {
    init_state axiom totalVotes() == 0;
    axiom totalVotes() >= 0;
}

// Original CVL declaration: ERC721Votes.spec:53-54
ghost lastFromBlock(address) returns uint32;

// Original CVL declaration: ERC721Votes.spec:55-57
ghost doubleFromBlock(address) returns bool {
    init_state axiom forall address a. doubleFromBlock(a) == false;
}

rule previous_delegatee_votes_removed() {
    env e;
    address delegator; address delegatee; address third;

    require third != delegatee;
    require delegates(delegator) == third;
    require numCheckpoints(third) < 1000000;

    uint256 delegator_bal = balanceOf(e, delegator);
    uint256 votes_ = getVotes(third);

    _delegate(e, delegator, delegatee);

    uint256 _votes = getVotes(third);

    assert third != 0x0 => _votes == votes_ - delegator_bal, "votes not removed from the previous delegatee";
}
