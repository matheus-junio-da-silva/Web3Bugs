// Project 10; source contracts/10/specs/proxy.spec; exact original rule startStateCleanup.
// Target-specific catalog context: HMaker; report check #31, physical PDF page 30.
// Historical driver: contracts/10/specs/scripts/runHMaker.sh; no independent historical proof is asserted.
// Selected CVL dependencies come from generic Example 15 and original source lines 9;17;357-366;580-584.

methods {
    getSlot(uint slot) returns (uint) envfree
    getStackLengthSlot() returns (uint256) envfree
}

function arbitrary(method f) {
    env e__;
    calldataarg arg__;
    f(e__, arg__);
}

rule startStateCleanup(method f, uint slot) {
    uint oldValue = getSlot(slot);

    arbitrary(f);

    uint newValue = getSlot(slot);

    // slot 0 is stack length, which we ignore because some handlers are pushing entries into the stack
    assert oldValue == 0 => (newValue == 0 || slot == getStackLengthSlot()), "Start state of $slot which is not stack length was not cleaned up";
}
