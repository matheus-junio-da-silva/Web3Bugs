// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155.spec lines 779-806
// Target: ERC1155Mock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155.spec:3-10
methods {
    balanceOf(address, uint256) returns(uint256) envfree
    safeTransferFrom(address, address, uint256, uint256, bytes)
    safeBatchTransferFrom(address, address, uint256[], uint256[], bytes)
}

rule singleTokenSafeTransferFromSafeBatchTransferFromEquivalence {
    storage beforeTransfer = lastStorage;
    env e;

    address holder; address recipient;
    uint256 token; uint256 transferAmount; bytes data;
    uint256[] tokens; uint256[] transferAmounts;

    mathint holderStartingBalance = balanceOf(holder, token);
    mathint recipientStartingBalance = balanceOf(recipient, token);

    require tokens.length == 1; require transferAmounts.length == 1;
    require tokens[0] == token; require transferAmounts[0] == transferAmount;

    // transferring via safeTransferFrom
    safeTransferFrom(e, holder, recipient, token, transferAmount, data) at beforeTransfer;
    mathint holderSafeTransferFromBalanceChange = holderStartingBalance - balanceOf(holder, token);
    mathint recipientSafeTransferFromBalanceChange = balanceOf(recipient, token) - recipientStartingBalance;

    // transferring via safeBatchTransferFrom
    safeBatchTransferFrom(e, holder, recipient, tokens, transferAmounts, data) at beforeTransfer;
    mathint holderSafeBatchTransferFromBalanceChange = holderStartingBalance - balanceOf(holder, token);
    mathint recipientSafeBatchTransferFromBalanceChange = balanceOf(recipient, token) - recipientStartingBalance;

    assert holderSafeTransferFromBalanceChange == holderSafeBatchTransferFromBalanceChange
        && recipientSafeTransferFromBalanceChange == recipientSafeBatchTransferFromBalanceChange, 
        "Transferring a single token via safeTransferFrom or safeBatchTransferFrom must be equivalent";
}   
