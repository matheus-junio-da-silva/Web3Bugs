// Source: contracts/11/specs/fullyBackedBonding.spec
// Property: noFrontRunningOnWithdraw (original lines 360-402)
// Original CVL dependency source lines: 14,16,17,18,23,24,25,26,27,28;32-33;35-36;43;46;50-53;70-73;85-91;57-60;93-95;360-402
// Dependency status: incomplete; historical source syntax kept unchanged.

methods {
    balanceOf(address) returns uint256 envfree
    beneficiaryOf(address) returns address envfree
    bondAmount(address, address, uint256) returns uint256 envfree
    init_state() envfree
    ownerOf(address) returns address envfree
    seizeBond(address, uint, uint, address)
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

ghost allUnbonded() returns uint256
{
  init_state axiom allUnbonded() == 0;
}

hook Sstore unbondedValue[KEY uint operatorY] uint value (uint old_value) STORAGE {
    havoc allUnbonded assuming allUnbonded@new() == allUnbonded@old() + value - old_value;
}

rule noFrontRunningOnWithdraw(address operator, address owner, address beneficiary, address otherOperator, uint256 x,
        method f) {
    env eF;
    calldataarg args;
    uint256 referenceID;

    require ownerOf(operator) == owner && beneficiaryOf(operator) == beneficiary;
    require otherOperator != operator;

    require safeAdd(unbondedValue(operator), unbondedValue(otherOperator)) &&
            allUnbonded()  >= unbondedValue(operator) + unbondedValue(otherOperator);

    require safeAdd(totalLockedBonds(operator), totalLockedBonds(otherOperator)) &&
            allLockedBond()  >= totalLockedBonds(operator) + totalLockedBonds(otherOperator);

    require safeAdd(allUnbonded(), allLockedBond()) &&
            balanceOf(currentContract) >= allUnbonded() + allLockedBond();

    require totalLockedBonds(otherOperator) >= bondAmount(otherOperator, eF.msg.sender, referenceID);

    uint256 allUserAssets = allUnbonded() + allLockedBond();
    require safeAdd(balanceOf(currentContract), allUserAssets);
    uint256 allAssets = balanceOf(currentContract) + allUserAssets;
    require safeAdd(balanceOf(beneficiary), allAssets);
    require beneficiary != currentContract;

    storage init_storage = lastStorage;
    env eWithdraw;
    withdraw(eWithdraw, x, operator);
    bool succSceanrio1 = !lastReverted;

    // f should only change other operator and if changed totalLocked than the specific bondID used in the require
    uint256 u = unbondedValue(otherOperator) at init_storage;
    uint256 l = totalLockedBonds(otherOperator);
    uint256 bondBefore = bondAmount(otherOperator, eF.msg.sender, referenceID);
    f(eF, args);
    require u != unbondedValue(otherOperator) || l != totalLockedBonds(otherOperator);
    require f.selector==seizeBond(address,uint256,uint256,address).selector =>
                bondBefore != bondAmount(otherOperator, eF.msg.sender, referenceID);
    invoke withdraw(eWithdraw, x, operator);
    bool succSceanrio2 = !lastReverted;
    assert succSceanrio2;
}
