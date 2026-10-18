// Source: contracts/11/specs/fullyBackedBonding.spec
// Property: validChangeToBalanceOf (original lines 456-472)
// Original CVL dependency source lines: 14,16,20,25,27,28;456-472
// Dependency status: incomplete; historical source syntax kept unchanged.

methods {
    balanceOf(address) returns uint256 envfree
    deposit(address)
    seizeBond(address, uint, uint, address)
    withdraw(uint256, address)
}

rule validChangeToBalanceOf(address o, method f) {
    env e;
    calldataarg args;
    require (o != currentContract);
    uint256 before = balanceOf(o);
    f(e, args);
    uint256 after = balanceOf(o);
    assert before == after ||
        // depositing case
        ( (f.selector==topUp(address).selector || f.selector==deposit(address).selector ||
           f.selector==delegate(address, address, address).selector  ) &&
           after == before - e.msg.value ) ||
        // withdrawing case
           ( ( f.selector==seizeBond(address,uint256,uint256,address).selector ||
                f.selector==withdraw(uint256,address).selector) &&
           after >= before );
}
