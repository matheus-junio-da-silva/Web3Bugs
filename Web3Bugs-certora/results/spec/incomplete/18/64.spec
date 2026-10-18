// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC20FlashMint.spec lines 18-28
// Target: ERC20FlashMintMock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC20FlashMint.spec:8-9
ghost mapping(address => uint256) trackedBurnAmount;

rule letsWatchItBurns(env e){
    address receiver; address token; uint256 amount; bytes data;

    uint256 feeBefore = flashFee(e, token, amount);

    flashLoan(e, receiver, token, amount, data);

    uint256 burned = trackedBurnAmount[receiver];

    assert to_mathint(amount + feeBefore) == burned, "cheater";
}
