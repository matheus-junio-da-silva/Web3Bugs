// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC721Votes.spec lines 116-131
// Target: ERC721Votes (historical voting harness)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC721Votes.spec:5-19
methods {
    checkpoints(address, uint32) envfree
    numCheckpoints(address) returns (uint32) envfree
    ckptFromBlock(address, uint32) returns (uint32) envfree
}

// Original CVL declaration: ERC721Votes.spec:44-50
hook Sstore _checkpoints[KEY address account].votes uint224 newVotes (uint224 oldVotes) STORAGE {
    havoc userVotes assuming
        userVotes@new(account) == newVotes;

    havoc totalVotes assuming
        totalVotes@new() == totalVotes@old() + to_mathint(newVotes) - to_mathint(userVotes(account));
}

// Original CVL declaration: ERC721Votes.spec:55-57
ghost doubleFromBlock(address) returns bool {
    init_state axiom forall address a. doubleFromBlock(a) == false;
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

rule unique_checkpoints_rule(method f) {
    env e; calldataarg args;
    address account;
    uint32 num_ckpts_ = numCheckpoints(account); 
    uint32 fromBlock_ = num_ckpts_ == 0 ? 0 : ckptFromBlock(account, num_ckpts_ - 1);

    f(e, args);

    uint32 _num_ckpts = numCheckpoints(account);
    uint32 _fromBlock = _num_ckpts == 0 ? 0 : ckptFromBlock(account, _num_ckpts - 1);
    

    assert fromBlock_ == _fromBlock => num_ckpts_ == _num_ckpts || _num_ckpts == 1, "same fromBlock, new checkpoint";
    // this assert fails consistently
    // assert !doubleFromBlock(account) => ckpts_ != _ckpts, "new fromBlock but total checkpoints not being increased";
}
