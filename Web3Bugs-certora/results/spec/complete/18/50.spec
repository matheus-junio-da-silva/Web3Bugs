// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155Burnable.spec lines 102-138
// Target: ERC1155BurnableMock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155Burnable.spec:2-2
methods {
    balanceOf(address, uint256) returns uint256 envfree
}

rule multipleTokenBurnBurnBatchEquivalence {
    storage beforeBurns = lastStorage;
    env e;

    address holder;
    uint256 tokenA; uint256 tokenB; uint256 tokenC;
    uint256 burnAmountA; uint256 burnAmountB; uint256 burnAmountC;
    uint256[] tokens; uint256[] burnAmounts;

    mathint startingBalanceA = balanceOf(holder, tokenA);
    mathint startingBalanceB = balanceOf(holder, tokenB);
    mathint startingBalanceC = balanceOf(holder, tokenC);

    require tokens.length == 3; require burnAmounts.length == 3;
    require tokens[0] == tokenA; require burnAmounts[0] == burnAmountA;
    require tokens[1] == tokenB; require burnAmounts[1] == burnAmountB;
    require tokens[2] == tokenC; require burnAmounts[2] == burnAmountC;

    // burning via burn
    burn(e, holder, tokenA, burnAmountA) at beforeBurns;
    burn(e, holder, tokenB, burnAmountB);
    burn(e, holder, tokenC, burnAmountC);
    mathint burnBalanceChangeA = startingBalanceA - balanceOf(holder, tokenA);
    mathint burnBalanceChangeB = startingBalanceB - balanceOf(holder, tokenB);
    mathint burnBalanceChangeC = startingBalanceC - balanceOf(holder, tokenC);

    // burning via burnBatch
    burnBatch(e, holder, tokens, burnAmounts) at beforeBurns;
    mathint burnBatchBalanceChangeA = startingBalanceA - balanceOf(holder, tokenA);
    mathint burnBatchBalanceChangeB = startingBalanceB - balanceOf(holder, tokenB);
    mathint burnBatchBalanceChangeC = startingBalanceC - balanceOf(holder, tokenC);

    assert burnBalanceChangeA == burnBatchBalanceChangeA
        && burnBalanceChangeB == burnBatchBalanceChangeB
        && burnBalanceChangeC == burnBatchBalanceChangeC, 
        "Burning multiple tokens via burn or burnBatch must be equivalent";
}
