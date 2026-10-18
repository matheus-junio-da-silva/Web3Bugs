// Source: contracts/11/specs/fullyBackedBonding.spec
// Property: totalAssetsPreservedOnSeizeBond (original lines 254-263)
// Original CVL dependency source lines: 1;14,16,23,25,26,28;43;46;50-53;70-73;85-91;254-263
// Dependency status: incomplete; historical source syntax kept unchanged.

using OtherBeneficiary as otherBeneficiary

methods {
    balanceOf(address) returns uint256 envfree
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

rule totalAssetsPreservedOnSeizeBond(address operator, address owner, uint256 referenceID,
            uint256 amount, address destination) {
    env e;
    require destination == otherBeneficiary;
    mathint totalAssetsBefore = totalLockedBonds(operator) + unbondedValue(operator) + balanceOf(destination);
    seizeBond(e, operator, referenceID, amount, destination);
    mathint totalAssetsAfter = totalLockedBonds(operator) + unbondedValue(operator) + balanceOf(destination);
    assert  totalAssetsBefore == totalAssetsAfter,
        "seizeBond can change the total assets of operator in an unexpected way";
}
