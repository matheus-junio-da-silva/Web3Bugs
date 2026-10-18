// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC20Votes.spec lines 69-79
// Target: ERC20Votes (historical voting harness)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC20Votes.spec:4-22
methods {
    numCheckpoints(address) returns (uint32) envfree
    totalSupply() returns (uint256) envfree
    burn(address, uint256)
    _delegates(address) returns (address) envfree
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

invariant votes_solvency()
    totalSupply() >= to_uint256(totalVotes())
filtered { f -> f.selector != _burn(address, uint256).selector}
{ preserved with(env e) {
    require forall address account. numCheckpoints(account) < 1000000;
} preserved burn(address a, uint256 amount) with(env e){
    require _delegates(0) == 0;
    require forall address a2. (_delegates(a) != _delegates(a2)) && (balanceOf(e, _delegates(a)) + balanceOf(e, _delegates(a2)) <= totalVotes());
    require balanceOf(e, _delegates(a)) < totalVotes();
    require amount < 100000;
}}
