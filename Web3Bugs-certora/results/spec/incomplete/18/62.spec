// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155Supply.spec lines 56-59
// Target: ERC1155Supply (historical verification harness)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155Supply.spec:4-4
methods {
    balanceOf(address, uint256) returns uint256 envfree
}

// Original CVL declaration: ERC1155Supply.spec:39-41
hook Sstore _balances[KEY uint256 token][KEY address user] uint256 newValue (uint256 oldValue) STORAGE {
    sumOfBalances[token] = sumOfBalances[token] + newValue - oldValue;
}

// Original CVL declaration: ERC1155Supply.spec:35-37
ghost mapping(uint256 => mathint) sumOfBalances {
    init_state axiom forall uint256 token . sumOfBalances[token] == 0;
}

invariant balanceOfZeroAddressIsZero(uint256 token)
    balanceOf(0, token) == 0

/// If a user has a token, then the token should exist.

