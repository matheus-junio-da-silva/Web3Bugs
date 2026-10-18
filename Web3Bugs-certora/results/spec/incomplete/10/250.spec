// Project 10; source contracts/10/specs/proxy.spec; exact original rule senderIsAlwaysCleanedUp.
// Target-specific catalog context: HUniswapV2; report check #28, physical PDF page 27.
// Historical driver: contracts/10/specs/scripts/runHUniswapV2.sh; no independent historical proof is asserted.
// Selected CVL dependencies come from generic Example 18 and original source lines 11;393-401;580-584.

methods {
    getSender() returns (address) envfree
}

function arbitrary(method f) {
    env e__;
    calldataarg arg__;
    f(e__, arg__);
}

rule senderIsAlwaysCleanedUp(method f) {
    address before = getSender();

    arbitrary(f);

    address after = getSender();

    assert before == 0 => after == 0;
}
