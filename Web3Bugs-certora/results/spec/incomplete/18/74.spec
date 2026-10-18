// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC20Votes.spec lines 201-217
// Target: ERC20Votes (historical voting harness)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC20Votes.spec:4-10
methods {
    numCheckpoints(address) returns (uint32) envfree
    delegates(address) returns (address) envfree
    getVotes(address) returns (uint256) envfree
    _delegate(address, address)
}

// Original CVL declaration: ERC20Votes.spec:38-47
hook Sstore _checkpoints[KEY address account][INDEX uint32 index].votes uint224 newVotes (uint224 oldVotes) STORAGE {    
    havoc userVotes assuming
        userVotes@new(account) == newVotes;

    havoc totalVotes assuming
        totalVotes@new() == totalVotes@old() + newVotes - userVotes(account);

    havoc lastIndex assuming
        lastIndex@new(account) == index;
}

// Original CVL declaration: ERC20Votes.spec:59-65
hook Sstore _checkpoints[KEY address account][INDEX uint32 index].fromBlock uint32 newBlock (uint32 oldBlock) STORAGE {
    havoc lastFromBlock assuming
        lastFromBlock@new(account) == newBlock;
    
    havoc doubleFromBlock assuming 
        doubleFromBlock@new(account) == (newBlock == lastFromBlock(account));
}

// Original CVL declaration: ERC20Votes.spec:27-29
ghost userVotes(address) returns uint224 {
    init_state axiom forall address a. userVotes(a) == 0;
}

// Original CVL declaration: ERC20Votes.spec:32-34
ghost totalVotes() returns uint224 {
    init_state axiom totalVotes() == 0;
}

// Original CVL declaration: ERC20Votes.spec:35-37
ghost lastIndex(address) returns uint32;
// helper

// Original CVL declaration: ERC20Votes.spec:50-51
ghost lastFromBlock(address) returns uint32;

// Original CVL declaration: ERC20Votes.spec:52-54
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
