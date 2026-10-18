// Project 10; source contracts/10/specs/proxy.spec; exact original rule stackLengthIncreaseIsBounded.
// Target-specific catalog context: HOneInchExchange; report check #27, physical PDF page 26.
// Historical driver: no matching historical per-target launcher preserved; no independent historical proof is asserted.
// Selected CVL dependencies come from generic Example 17 and original source lines 13;334;384-391;580-584.

methods {
    getStackLength() returns (uint256) envfree
}

definition STACK_INCREASE_BOUND() returns uint256 = 1000000 ;    // 1 million

function arbitrary(method f) {
    env e__;
    calldataarg arg__;
    f(e__, arg__);
}

rule stackLengthIncreaseIsBounded(method f) {
    uint256 stackLengthBefore = getStackLength();

    arbitrary(f);

    uint256 stackLengthAfter = getStackLength();
    assert stackLengthAfter <= stackLengthBefore + STACK_INCREASE_BOUND(), "Found a way to increase stack length by more than 1 million";
}
