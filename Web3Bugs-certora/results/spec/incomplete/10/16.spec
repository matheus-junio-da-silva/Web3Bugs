// Project 10 — literal active noOverwrite from contracts/10/specs/proxy.spec:370-381
// CVL dependencies selected by transitive reference; historical CVL syntax is not migrated.
// Snapshot is not an executable proof of the 2021 audit.


methods {
    getSlot(uint slot) returns (uint) envfree
    getStackLength() returns (uint256) envfree
    getStackLengthSlot() returns (uint256) envfree
}

definition MAX_UINT256() returns uint256 = 115792089237316195423570985008687907853269984665640564039457584007913129639935
    ;

definition STACK_INCREASE_BOUND() returns uint256 = 1000000 ;    // 1 million

function arbitrary(method f) {
    env e__;
    calldataarg arg__;
    f(e__, arg__);
}

rule noOverwrite(method f, uint slot) {
    require getStackLength() < MAX_UINT256() - STACK_INCREASE_BOUND(); // see stackLengthIncreaseIsBounded
    uint oldValue = getSlot(slot);

    arbitrary(f);

    uint newValue = getSlot(slot);
    
    // slot 0 is stack length, postProcess() may nullify it and it's fine, and execs() can increase it
    assert oldValue != 0 => (newValue == oldValue 
            || slot == getStackLengthSlot()), "Slot $slot changd during this execution";
}
