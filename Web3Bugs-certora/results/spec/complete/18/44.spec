// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155.spec lines 810-858
// Target: ERC1155Mock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155.spec:3-10
methods {
    balanceOf(address, uint256) returns(uint256) envfree
    safeTransferFrom(address, address, uint256, uint256, bytes)
    safeBatchTransferFrom(address, address, uint256[], uint256[], bytes)
}

rule multipleTokenSafeTransferFromSafeBatchTransferFromEquivalence {
    storage beforeTransfers = lastStorage;
    env e;

    address holder; address recipient; bytes data;
    uint256 tokenA; uint256 tokenB; uint256 tokenC;
    uint256 transferAmountA; uint256 transferAmountB; uint256 transferAmountC;
    uint256[] tokens; uint256[] transferAmounts;

    mathint holderStartingBalanceA = balanceOf(holder, tokenA);
    mathint holderStartingBalanceB = balanceOf(holder, tokenB);
    mathint holderStartingBalanceC = balanceOf(holder, tokenC);
    mathint recipientStartingBalanceA = balanceOf(recipient, tokenA);
    mathint recipientStartingBalanceB = balanceOf(recipient, tokenB);
    mathint recipientStartingBalanceC = balanceOf(recipient, tokenC);

    require tokens.length == 3; require transferAmounts.length == 3;
    require tokens[0] == tokenA; require transferAmounts[0] == transferAmountA;
    require tokens[1] == tokenB; require transferAmounts[1] == transferAmountB;
    require tokens[2] == tokenC; require transferAmounts[2] == transferAmountC;

    // transferring via safeTransferFrom
    safeTransferFrom(e, holder, recipient, tokenA, transferAmountA, data) at beforeTransfers;
    safeTransferFrom(e, holder, recipient, tokenB, transferAmountB, data);
    safeTransferFrom(e, holder, recipient, tokenC, transferAmountC, data);
    mathint holderSafeTransferFromBalanceChangeA = holderStartingBalanceA - balanceOf(holder, tokenA);
    mathint holderSafeTransferFromBalanceChangeB = holderStartingBalanceB - balanceOf(holder, tokenB);
    mathint holderSafeTransferFromBalanceChangeC = holderStartingBalanceC - balanceOf(holder, tokenC);
    mathint recipientSafeTransferFromBalanceChangeA = balanceOf(recipient, tokenA) - recipientStartingBalanceA;
    mathint recipientSafeTransferFromBalanceChangeB = balanceOf(recipient, tokenB) - recipientStartingBalanceB;
    mathint recipientSafeTransferFromBalanceChangeC = balanceOf(recipient, tokenC) - recipientStartingBalanceC;

    // transferring via safeBatchTransferFrom
    safeBatchTransferFrom(e, holder, recipient, tokens, transferAmounts, data) at beforeTransfers;
    mathint holderSafeBatchTransferFromBalanceChangeA = holderStartingBalanceA - balanceOf(holder, tokenA);
    mathint holderSafeBatchTransferFromBalanceChangeB = holderStartingBalanceB - balanceOf(holder, tokenB);
    mathint holderSafeBatchTransferFromBalanceChangeC = holderStartingBalanceC - balanceOf(holder, tokenC);
    mathint recipientSafeBatchTransferFromBalanceChangeA = balanceOf(recipient, tokenA) - recipientStartingBalanceA;
    mathint recipientSafeBatchTransferFromBalanceChangeB = balanceOf(recipient, tokenB) - recipientStartingBalanceB;
    mathint recipientSafeBatchTransferFromBalanceChangeC = balanceOf(recipient, tokenC) - recipientStartingBalanceC;

    assert holderSafeTransferFromBalanceChangeA == holderSafeBatchTransferFromBalanceChangeA
        && holderSafeTransferFromBalanceChangeB == holderSafeBatchTransferFromBalanceChangeB
        && holderSafeTransferFromBalanceChangeC == holderSafeBatchTransferFromBalanceChangeC
        && recipientSafeTransferFromBalanceChangeA == recipientSafeBatchTransferFromBalanceChangeA
        && recipientSafeTransferFromBalanceChangeB == recipientSafeBatchTransferFromBalanceChangeB
        && recipientSafeTransferFromBalanceChangeC == recipientSafeBatchTransferFromBalanceChangeC, 
        "Transferring multiple tokens via safeTransferFrom or safeBatchTransferFrom must be equivalent";
}
