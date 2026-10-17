// Project 10 — literal active startStateCleanup from contracts/10/specs/proxy.spec:357-366
// CVL dependencies selected by transitive reference; historical CVL syntax is not migrated.
// Snapshot is not an executable proof of the 2021 audit.


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
