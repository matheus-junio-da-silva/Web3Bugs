// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC20Votes.spec lines 236-271
// Target: ERC20Votes (historical voting harness)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC20Votes.spec:4-10
methods {
    numCheckpoints(address) returns (uint32) envfree
    delegates(address) returns (address) envfree
    getVotes(address) returns (uint256) envfree
    delegate(address)
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

rule delegate_no_frontrunning(method f) {
    env e; calldataarg args;
    address delegator; address delegatee; address third; address other;



    require numCheckpoints(delegatee) < 1000000;
    require numCheckpoints(third) < 1000000;


    f(e, args);

    uint256 delegator_bal = balanceOf(e, delegator);
    uint256 delegatee_votes_ = getVotes(delegatee);
    uint256 third_votes_ = getVotes(third);
    uint256 other_votes_ = getVotes(other);
    require delegates(delegator) == third;
    require third != delegatee;
    require other != third;
    require other != delegatee;
    require delegatee != 0x0;

    _delegate(e, delegator, delegatee);

    uint256 _delegatee_votes = getVotes(delegatee);
    uint256 _third_votes = getVotes(third);
    uint256 _other_votes = getVotes(other);


    // previous delegatee loses all of their votes
    // delegatee gains that many votes
    // third loses any votes delegated to them
    assert _delegatee_votes == delegatee_votes_ + delegator_bal, "delegatee did not receive votes";
    assert third != 0 => _third_votes == third_votes_ - delegator_bal, "votes not removed from third";
    assert other_votes_ == _other_votes, "delegate not contained";
}
