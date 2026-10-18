// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155Burnable.spec lines 26-45
// Target: ERC1155BurnableMock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155Burnable.spec:2-2
methods {
    balanceOf(address, uint256) returns uint256 envfree
}

rule burnAmountProportionalToBalanceReduction {
    storage beforeBurn = lastStorage;
    env e;
    
    address holder; uint256 token;
    mathint startingBalance = balanceOf(holder, token);
    uint256 smallBurn; uint256 largeBurn;
    require smallBurn < largeBurn;

    // smaller burn amount
    burn(e, holder, token, smallBurn) at beforeBurn;
    mathint smallBurnBalanceChange = startingBalance - balanceOf(holder, token);

    // larger burn amount
    burn(e, holder, token, largeBurn) at beforeBurn;
    mathint largeBurnBalanceChange = startingBalance - balanceOf(holder, token);

    assert smallBurnBalanceChange < largeBurnBalanceChange, 
        "A larger burn must lead to a larger decrease in balance";
}
