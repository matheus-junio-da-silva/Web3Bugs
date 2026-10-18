// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155Supply.spec lines 11-31
// Target: ERC1155Supply (historical verification harness)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155Supply.spec:3-6
methods {
    totalSupply(uint256) returns uint256 envfree
    owner() returns address envfree
}

// Original CVL declaration: ERC1155Supply.spec:39-41
hook Sstore _balances[KEY uint256 token][KEY address user] uint256 newValue (uint256 oldValue) STORAGE {
    sumOfBalances[token] = sumOfBalances[token] + newValue - oldValue;
}

// Original CVL declaration: ERC1155Supply.spec:35-37
ghost mapping(uint256 => mathint) sumOfBalances {
    init_state axiom forall uint256 token . sumOfBalances[token] == 0;
}

rule token_totalSupply_independence(method f)
filtered {
    f -> f.selector != safeBatchTransferFrom(address,address,uint256[],uint256[],bytes).selector
}
{
    uint256 token1; uint256 token2;
    require token1 != token2;

    uint256 token1_before = totalSupply(token1);
    uint256 token2_before = totalSupply(token2);

    env e; calldataarg args;
    require e.msg.sender != owner(); // owner can call mintBatch and burnBatch in our harness
    f(e, args);

    uint256 token1_after = totalSupply(token1);
    uint256 token2_after = totalSupply(token2);

    assert token1_after != token1_before => token2_after == token2_before,
        "methods must not change the total supply of more than one token";
}
