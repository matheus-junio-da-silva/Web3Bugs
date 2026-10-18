// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155Supply.spec lines 60-71
// Target: ERC1155Supply (historical verification harness)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155Supply.spec:3-5
methods {
    totalSupply(uint256) returns uint256 envfree
    balanceOf(address, uint256) returns uint256 envfree
    exists_wrapper(uint256) returns bool envfree
}

// Original CVL declaration: ERC1155Supply.spec:39-41
hook Sstore _balances[KEY uint256 token][KEY address user] uint256 newValue (uint256 oldValue) STORAGE {
    sumOfBalances[token] = sumOfBalances[token] + newValue - oldValue;
}

// Original CVL declaration: ERC1155Supply.spec:45-51
invariant total_supply_is_sum_of_balances(uint256 token)
    sumOfBalances[token] == totalSupply(token)
    {
        preserved {
            requireInvariant balanceOfZeroAddressIsZero(token);
        }
    }

// Original CVL declaration: ERC1155Supply.spec:56-59
invariant balanceOfZeroAddressIsZero(uint256 token)
    balanceOf(0, token) == 0

/// If a user has a token, then the token should exist.

// Original CVL declaration: ERC1155Supply.spec:35-37
ghost mapping(uint256 => mathint) sumOfBalances {
    init_state axiom forall uint256 token . sumOfBalances[token] == 0;
}

rule held_tokens_should_exist {
    address user; uint256 token;

    requireInvariant balanceOfZeroAddressIsZero(token);

    // This assumption is safe because of total_supply_is_sum_of_balances
    require balanceOf(user, token) <= totalSupply(token);

    // note: `exists_wrapper` just calls `exists`
    assert balanceOf(user, token) > 0 => exists_wrapper(token),
        "if a user's balance for a token is positive, the token must exist";
}
