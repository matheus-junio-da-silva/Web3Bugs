// Source: contracts/11/specs/fullyBackedBonding.spec
// Property: totalAssetsPreservedOnWithdraw (original lines 236-244)
// Original CVL dependency source lines: 14,16,17,23,26,27,28;43;46;50-53;70-73;85-91;236-244
// Dependency status: incomplete; historical source syntax kept unchanged.

methods {
    balanceOf(address) returns uint256 envfree
    beneficiaryOf(address) returns address envfree
    init_state() envfree
    unbondedValue(address) returns uint256 envfree
    withdraw(uint256, address)
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

rule totalAssetsPreservedOnWithdraw(address operator, address owner, address beneficiary, uint256 amount) {
     env e;
     require beneficiaryOf(operator) == beneficiary;
     require beneficiary != currentContract;
     mathint totalAssets = totalLockedBonds(operator) + unbondedValue(operator) + balanceOf(beneficiary);
     withdraw(e, amount, operator);
     assert totalAssets == totalLockedBonds(operator) + unbondedValue(operator) + balanceOf(beneficiary),
     "withdraw can change the total assets of an operator in an unexpected way";
}
