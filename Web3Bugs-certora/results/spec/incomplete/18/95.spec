// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC721Votes.spec lines 137-161
// Target: ERC721Votes (historical voting harness)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC721Votes.spec:6-11
methods {
    numCheckpoints(address) returns (uint32) envfree
    getVotes(address) returns (uint256) envfree
    delegates(address) returns (address) envfree
    delegate(address)
}

// Original CVL declaration: ERC721Votes.spec:39-42
ghost totalVotes() returns mathint {
    init_state axiom totalVotes() == 0;
    axiom totalVotes() >= 0;
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

// Original CVL declaration: ERC721Votes.spec:53-54
ghost lastFromBlock(address) returns uint32;

// Original CVL declaration: ERC721Votes.spec:55-57
ghost doubleFromBlock(address) returns bool {
    init_state axiom forall address a. doubleFromBlock(a) == false;
}

rule transfer_safe() {
    env e;
    uint256 ID;
    address a; address b;

    require delegates(a) != delegates(b); // confirmed if they both delegate to the same person then transfer keeps the votes the same
    require numCheckpoints(delegates(a)) < 1000000;
    require numCheckpoints(delegates(b)) < 1000000;

    uint256 votesA_pre = getVotes(delegates(a));
    uint256 votesB_pre = getVotes(delegates(b));

    mathint totalVotes_pre = totalVotes();

    transferFrom(e, a, b, ID);
    
    mathint totalVotes_post = totalVotes();
    uint256 votesA_post = getVotes(delegates(a));
    uint256 votesB_post = getVotes(delegates(b));

    // if an account that has not delegated transfers balance to an account that has, it will increase the total supply of votes
    assert totalVotes_pre == totalVotes_post, "transfer changed total supply";
    assert delegates(a) != 0 => votesA_pre - 1 == votesA_post, "A lost the wrong amount of votes";
    assert delegates(b) != 0 => votesB_pre + 1 == votesB_post, "B gained the wrong amount of votes";
}
