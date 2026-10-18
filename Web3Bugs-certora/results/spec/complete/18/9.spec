// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155.spec lines 87-103
// Target: ERC1155Mock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155.spec:3-14
methods {
    balanceOf(address, uint256) returns(uint256) envfree
    safeTransferFrom(address, address, uint256, uint256, bytes)
    safeBatchTransferFrom(address, address, uint256[], uint256[], bytes)
    mint(address, uint256, uint256, bytes)
    mintBatch(address, uint256[], uint256[], bytes)
    burn(address, uint256, uint256)
    burnBatch(address, uint256[], uint256[])
}

rule unexpectedBalanceChange(method f, env e) 
    filtered { f -> f.selector != safeTransferFrom(address, address, uint256, uint256, bytes).selector
                        && f.selector != safeBatchTransferFrom(address, address, uint256[], uint256[], bytes).selector 
                        && f.selector != mint(address, uint256, uint256, bytes).selector 
                        && f.selector != mintBatch(address, uint256[], uint256[], bytes).selector  
                        && f.selector != burn(address, uint256, uint256).selector 
                        && f.selector != burnBatch(address, uint256[], uint256[]).selector } {
    address from; uint256 id;
    uint256 balanceBefore = balanceOf(from, id);

    calldataarg args;
    f(e, args);

    uint256 balanceAfter = balanceOf(from, id);

    assert balanceBefore == balanceAfter, "How you dare to take my money?";
}
