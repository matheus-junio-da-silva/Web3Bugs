// Source: contracts/11/specs/fullyBackedBonding.spec
// Property: maximalWithdraw (original lines 303-311)
// Original CVL dependency source lines: 14,21,23,26,27,28;32-33;35-36;43;46;50-53;70-73;85-91;303-311
// Dependency status: incomplete; historical source syntax kept unchanged.

methods {
    everDeposited(address) returns uint256 envfree
    init_state() envfree
    unbondedValue(address) returns uint256 envfree
    withdraw(uint256, address)
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

rule maximalWithdraw(address operator) {
    env e;
    require safeAdd(unbondedValue(operator), totalLockedBonds(operator));
    require everDeposited(operator) >= (unbondedValue(operator) + totalLockedBonds(operator));
    uint256 x = everDeposited(operator);
    invoke withdraw(e, x, operator);
    assert !lastReverted => (unbondedValue(operator) == 0 && totalLockedBonds(operator)==0),
            "maximum withdraw does not hold";
}
