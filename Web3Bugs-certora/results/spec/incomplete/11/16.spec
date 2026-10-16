// Source: contracts/11/specs/fullyBackedBonding.spec
// Property: validChangeToEverDeposited (original lines 550-560)
// Original CVL dependency source lines: 14,20,21,28;550-560
// Dependency status: incomplete; historical source syntax kept unchanged.

methods {
    deposit(address)
    everDeposited(address) returns uint256 envfree
}

rule validChangeToEverDeposited(address o,  method f) {
    env e;
    calldataarg args;
    uint256 before = everDeposited(o);
    f(e, args);
    uint256 after = everDeposited(o);
    assert after == before ||
           ( ( f.selector==topUp(address).selector || f.selector==deposit(address).selector ||
               f.selector==delegate(address, address, address).selector ) &&
               after == before + e.msg.value );
}
