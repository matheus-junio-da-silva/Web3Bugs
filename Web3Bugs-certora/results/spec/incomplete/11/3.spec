// Source: contracts/11/specs/fullyBackedBonding.spec
// Property: noBankruptcy (original lines 161-175)
// Original CVL dependency source lines: 14,16,20,23,28;43;46;50-53;70-73;85-91;57-60;93-95;161-175
// Dependency status: incomplete; historical source syntax kept unchanged.

methods {
    balanceOf(address) returns uint256 envfree
    deposit(address)
    init_state() envfree
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

ghost allUnbonded() returns uint256
{
  init_state axiom allUnbonded() == 0;
}

hook Sstore unbondedValue[KEY uint operatorY] uint value (uint old_value) STORAGE {
    havoc allUnbonded assuming allUnbonded@new() == allUnbonded@old() + value - old_value;
}

invariant noBankruptcy()
    (allUnbonded() + allLockedBond()) <= balanceOf(currentContract) {
    preserved deposit(env e, address operator) {
        require e.msg.sender != currentContract;
        require (allUnbonded() + allLockedBond()) <= balanceOf(currentContract);
    }
    preserved topUp(env e, address _) {
        require e.msg.sender != currentContract;
        require (allUnbonded() + allLockedBond()) <= balanceOf(currentContract);
    }
    preserved delegate(env e, address _1 ,address _2, address _3) {
        require e.msg.sender != currentContract;
        require (allUnbonded() + allLockedBond()) <= balanceOf(currentContract);
    }
}
