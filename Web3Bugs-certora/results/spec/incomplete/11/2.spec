// Source: contracts/11/specs/fullyBackedBonding.spec
// Property: validState (original lines 115-150)
// Original CVL dependency source lines: 14,17,18,23,24,25,26,28;32-33;35-36;43;46;50-53;70-73;85-91;104-105;115-150
// Dependency status: incomplete; historical source syntax kept unchanged.

methods {
    beneficiaryOf(address) returns address envfree
    bondAmount(address, address, uint256) returns uint256 envfree
    init_state() envfree
    ownerOf(address) returns address envfree
    seizeBond(address, uint, uint, address)
    unbondedValue(address) returns uint256 envfree
}

definition MAXINT() returns uint256 =
        0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF;

definition safeAdd(uint256 x, uint256 y) returns bool =
        x + y >= y && x + y >=x && x+y <= MAXINT();

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

invariant validOperator(address operator)
        beneficiaryOf(operator) != 0  <=>  ( operator != 0 && ownerOf(operator) != 0 && authorizerOf(operator) != 0 )

rule validState(address operator, uint unbonded, uint totalLocked) {
     env e;
     require unbondedValue(operator) == unbonded;
     require totalLockedBonds(operator) == totalLocked;
     require safeAdd(unbonded, totalLocked);

     uint sum_before = unbonded + totalLocked;
     require safeAdd(sum_before, e.msg.value);

     require sum_before > 0 => beneficiaryOf(operator) != 0 ;
     require e.msg.sender != 0;
     require operator != 0;
     requireInvariant validOperator(operator);

     method f;
     if (f.selector != seizeBond(address, uint256, uint256, address).selector) {
        calldataarg args;
        f(e, args);

     } else {

        address seizeAddress;
        uint refID;
        uint amount;
        address destination;

        uint256 before = bondAmount(operator, e.msg.sender, refID);
        require totalLocked >= before;

        seizeBond(e, seizeAddress, refID, amount, destination);
     }

     uint sum_after = unbondedValue(operator) + totalLockedBonds(operator);
     assert sum_after > 0 =>
                ( ownerOf(operator) != 0 && beneficiaryOf(operator) != 0 );
}
