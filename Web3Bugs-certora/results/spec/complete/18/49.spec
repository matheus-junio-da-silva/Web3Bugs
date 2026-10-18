// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155Burnable.spec lines 75-98
// Target: ERC1155BurnableMock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155Burnable.spec:2-2
methods {
    balanceOf(address, uint256) returns uint256 envfree
}

rule singleTokenBurnBurnBatchEquivalence {
    storage beforeBurn = lastStorage;
    env e;

    address holder;
    uint256 token; uint256 burnAmount;
    uint256[] tokens; uint256[] burnAmounts;

    mathint startingBalance = balanceOf(holder, token);

    require tokens.length == 1; require burnAmounts.length == 1;
    require tokens[0] == token; require burnAmounts[0] == burnAmount;

    // burning via burn
    burn(e, holder, token, burnAmount) at beforeBurn;
    mathint burnBalanceChange = startingBalance - balanceOf(holder, token);

    // burning via burnBatch
    burnBatch(e, holder, tokens, burnAmounts) at beforeBurn;
    mathint burnBatchBalanceChange = startingBalance - balanceOf(holder, token);

    assert burnBalanceChange == burnBatchBalanceChange, 
        "Burning a single token via burn or burnBatch must be equivalent";
}   
