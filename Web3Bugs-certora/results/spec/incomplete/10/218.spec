// Project 10; source contracts/10/specs/proxy.spec; exact original rule noOverwrite.
// Target-specific catalog context: HGasTokens; report check #32, physical PDF page 31.
// Historical driver: contracts/10/specs/scripts/runHGasTokens.sh; no independent historical proof is asserted.
// Selected CVL dependencies come from generic Example 16 and original source lines 9;13;17;331-332;334;370-381;580-584.

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
