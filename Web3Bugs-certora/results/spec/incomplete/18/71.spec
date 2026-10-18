// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC20Votes.spec lines 145-164
// Target: ERC20Votes (historical voting harness)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC20Votes.spec:4-9
methods {
    numCheckpoints(address) returns (uint32) envfree
    delegates(address) returns (address) envfree
    getVotes(address) returns (uint256) envfree
    delegate(address)
}

// Original CVL declaration: ERC20Votes.spec:32-34
ghost totalVotes() returns uint224 {
    init_state axiom totalVotes() == 0;
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

// Original CVL declaration: ERC20Votes.spec:35-37
ghost lastIndex(address) returns uint32;
// helper

// Original CVL declaration: ERC20Votes.spec:50-51
ghost lastFromBlock(address) returns uint32;

// Original CVL declaration: ERC20Votes.spec:52-54
ghost doubleFromBlock(address) returns bool {
    init_state axiom forall address a. doubleFromBlock(a) == false;
}

rule transfer_safe() {
    env e;
    uint256 amount;
    address a; address b;
    require delegates(a) != delegates(b); // confirmed if they both delegate to the same person then transfer keeps the votes the same
    require numCheckpoints(delegates(a)) < 1000000;
    require numCheckpoints(delegates(b)) < 1000000;
    uint256 votesA_pre = getVotes(delegates(a));
    uint256 votesB_pre = getVotes(delegates(b));
    uint224 totalVotes_pre = totalVotes();
    transferFrom(e, a, b, amount);
    
    uint224 totalVotes_post = totalVotes();
    uint256 votesA_post = getVotes(delegates(a));
    uint256 votesB_post = getVotes(delegates(b));
    // if an account that has not delegated transfers balance to an account that has, it will increase the total supply of votes
    assert totalVotes_pre == totalVotes_post, "transfer changed total supply";
    assert delegates(a) != 0 => votesA_pre - votesA_post == amount, "A lost the wrong amount of votes";
    assert delegates(b) != 0 => votesB_post - votesB_pre == amount, "B lost the wrong amount of votes";
}
