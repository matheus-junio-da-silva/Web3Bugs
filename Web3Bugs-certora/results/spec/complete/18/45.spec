// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155.spec lines 861-878
// Target: ERC1155Mock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155.spec:10-10
methods {
    safeBatchTransferFrom(address, address, uint256[], uint256[], bytes)
}

rule transfersHaveSameLengthInputArrays {
    env e;

    address recipient; bytes data;
    uint256[] tokens; uint256[] transferAmounts;
    uint max_int = 0xffffffffffffffffffffffffffffffff;

    require tokens.length >= 0 && tokens.length <= max_int;
    require transferAmounts.length >= 0 && transferAmounts.length <= max_int;

    safeBatchTransferFrom(e, _, recipient, tokens, transferAmounts, data);

    uint256 tokensLength = tokens.length;
    uint256 transferAmountsLength = transferAmounts.length;

    assert tokens.length == transferAmounts.length, 
        "If transfer methods do not revert, the input arrays must be the same length";
}
