// Source: contracts/11/specs/fullyBackedBonding.spec
// Property: validChangeToUnbondedValue (original lines 519-538)
// Original CVL dependency source lines: 14,19,20,24,26,27,28;519-538
// Dependency status: incomplete; historical source syntax kept unchanged.

methods {
    createBond(address, address, uint256, uint256, address)
    deposit(address)
    ownerOf(address) returns address envfree
    unbondedValue(address) returns uint256 envfree
    withdraw(uint256, address)
}

rule validChangeToUnbondedValue(address o, address owner,  method f) {
    uint256 unbondedBefore = unbondedValue(o);
    env e;
    calldataarg args;
    f(e, args);
    uint256 unbondedAfter = unbondedValue(o);
    assert  unbondedAfter  == unbondedBefore ||
        //cases for deposit
        (( f.selector==topUp(address).selector || f.selector==deposit(address).selector ||
           f.selector==delegate(address, address, address).selector  ) &&
           unbondedAfter == unbondedBefore + e.msg.value ) ||
        //cases for withdraw
        ( f.selector==withdraw(uint256,address).selector && (e.msg.sender==o || e.msg.sender == ownerOf(o)) &&
          unbondedAfter <= unbondedBefore) ||
        // cases for holder free
        ( f.selector==freeBond(address,uint256).selector &&  unbondedAfter >= unbondedBefore ) ||
        // case for holder locking
        ( f.selector==createBond(address,address,uint256,uint256,address).selector &&
           unbondedAfter <= unbondedBefore );
}
