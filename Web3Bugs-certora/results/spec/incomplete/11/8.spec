// Source: contracts/11/specs/fullyBackedBonding.spec
// Property: integrityOfWithdraw (original lines 280-293)
// Original CVL dependency source lines: 14,16,17,21,23,26,27,28;32-33;35-36;43;46;50-53;70-73;85-91;280-293
// Dependency status: incomplete; historical source syntax kept unchanged.

methods {
    balanceOf(address) returns uint256 envfree
    beneficiaryOf(address) returns address envfree
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

rule integrityOfWithdraw(address operator,address beneficiary, uint256 x) {
    env e;
    require beneficiaryOf(operator) == beneficiary;
    require beneficiary != currentContract;
    require safeAdd(unbondedValue(operator),totalLockedBonds(operator));
    require everDeposited(operator) >= unbondedValue(operator) + totalLockedBonds(operator);
    uint256 u = unbondedValue(operator);
    uint256 b = balanceOf(beneficiary) ;
    uint s = balanceOf(currentContract);
    withdraw(e, x, operator);
    assert u - x == unbondedValue(operator) &&  b + x == balanceOf(beneficiary) &&
           s - x == balanceOf(currentContract) && x <= u && x <= everDeposited(operator),
           "withdraw integrity does not hold";
}
