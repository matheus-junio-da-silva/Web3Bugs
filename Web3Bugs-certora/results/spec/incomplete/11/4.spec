// Source: contracts/11/specs/fullyBackedBonding.spec
// Property: assetsLessThanEverDepositedAsRule (original lines 183-200)
// Original CVL dependency source lines: 14,18,19,21,23,25,26,28;32-33;35-36;43;46;50-53;70-73;85-91;183-200
// Dependency status: incomplete; historical source syntax kept unchanged.

methods {
    bondAmount(address, address, uint256) returns uint256 envfree
    createBond(address, address, uint256, uint256, address)
    everDeposited(address) returns uint256 envfree
    init_state() envfree
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

rule assetsLessThanEverDepositedAsRule(address operator, method f, mathint t, address holder, uint256 referenceID ) {
    env e;
    calldataarg args;
    require t == totalLockedBonds(operator);
    require totalLockedBonds(operator) >= bondAmount(operator, e.msg.sender, referenceID);
    require safeAdd(unbondedValue(operator), totalLockedBonds(operator));
    require everDeposited(operator) >= unbondedValue(operator) + totalLockedBonds(operator);
    require f.selector==init_state().selector => totalLockedBonds(operator)==0;
    uint256 before = bondAmount(operator, e.msg.sender, referenceID);
    f(e, args);
    require (f.selector==freeBond(address,uint256).selector                             ||
             f.selector==seizeBond(address,uint256,uint256,address).selector            ||
             f.selector==createBond(address,address,uint256,uint256,address).selector   ||
             f.selector==reassignBond(address, uint256, address, uint256).selector )    =>
             before != bondAmount(operator, e.msg.sender, referenceID);
    assert safeAdd(unbondedValue(operator), totalLockedBonds(operator)) &&
            everDeposited(operator) >= unbondedValue(operator) + totalLockedBonds(operator);
   }
