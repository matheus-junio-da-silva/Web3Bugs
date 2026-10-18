// Source: contracts/11/specs/fullyBackedBonding.spec
// Property: validChangeToTotalBondAmount (original lines 487-504)
// Original CVL dependency source lines: 14,19,23,25,26,28;43;46;50-53;70-73;85-91;487-504
// Dependency status: incomplete; historical source syntax kept unchanged.

methods {
    createBond(address, address, uint256, uint256, address)
    init_state() envfree
    seizeBond(address, uint, uint, address)
    unbondedValue(address) returns uint256 envfree
}

ghost bondIDToOperator(uint256) returns address;

ghost totalLockedBonds(uint256) returns uint256;

ghost allLockedBond() returns uint256
{
    init_state axiom allLockedBond() == 0;
}

hook Sload uint bondID operatorHolderRefToBondID[KEY uint operatorY][KEY uint holder][KEY uint referenceID] STORAGE {
    havoc bondIDToOperator assuming bondIDToOperator@new(bondID) == operatorY &&
            (forall uint otherBondID. otherBondID != bondID => bondIDToOperator@new(otherBondID) == bondIDToOperator@old(otherBondID));
}

hook Sstore lockedBonds[KEY uint bondID] uint value (uint old_value) STORAGE {
    uint256 operatorX = bondIDToOperator(bondID);
    havoc totalLockedBonds assuming totalLockedBonds@new(operatorX) == totalLockedBonds@old(operatorX) + value - old_value &&
            (forall uint256 otherOperator. otherOperator != operatorX =>
                totalLockedBonds@new(otherOperator) == totalLockedBonds@old(otherOperator));
    havoc allLockedBond assuming allLockedBond@new() == allLockedBond@old() + value - old_value;
}

rule validChangeToTotalBondAmount(address o, method f) {
    uint256 lockedBondsBefore = totalLockedBonds(o) ;
    uint256 unbondedBefore = unbondedValue(o);
    env e;
    calldataarg args;
    f(e, args);
    uint256 lockedBondsAfter = totalLockedBonds(o);
    assert lockedBondsBefore == lockedBondsAfter ||
           // case of unlocking
           ( (f.selector==freeBond(address,uint256).selector ||
              f.selector==seizeBond(address,uint256,uint256,address).selector ) &&
              lockedBondsAfter <= lockedBondsBefore )
           ||
           // case of locking
           ( f.selector==createBond(address,address,uint256,uint256,address).selector &&
             lockedBondsAfter >= lockedBondsBefore && lockedBondsAfter <= lockedBondsBefore + unbondedBefore )
           ;
}
