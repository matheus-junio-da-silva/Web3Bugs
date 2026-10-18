// Project 10 — literal active stackLengthIncreaseIsBounded from contracts/10/specs/proxy.spec:384-391
// CVL dependencies selected by transitive reference; historical CVL syntax is not migrated.
// Snapshot is not an executable proof of the 2021 audit.


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
