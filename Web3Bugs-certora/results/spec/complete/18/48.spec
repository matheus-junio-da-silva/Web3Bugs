// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155Burnable.spec lines 51-71
// Target: ERC1155BurnableMock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155Burnable.spec:2-2
methods {
    balanceOf(address, uint256) returns uint256 envfree
}

rule sequentialBurnsEquivalentToSingleBurnOfSum {
    storage beforeBurns = lastStorage;
    env e;

    address holder; uint256 token;
    mathint startingBalance = balanceOf(holder, token);
    uint256 firstBurn; uint256 secondBurn; uint256 sumBurn;
    require sumBurn == firstBurn + secondBurn;

    // sequential burns
    burn(e, holder, token, firstBurn) at beforeBurns;
    burn(e, holder, token, secondBurn);
    mathint sequentialBurnsBalanceChange = startingBalance - balanceOf(holder, token);

    // burn of sum of sequential burns
    burn(e, holder, token, sumBurn) at beforeBurns;
    mathint sumBurnBalanceChange = startingBalance - balanceOf(holder, token);

    assert sequentialBurnsBalanceChange == sumBurnBalanceChange, 
        "Sequential burns must be equivalent to a burn of their sum";
}
