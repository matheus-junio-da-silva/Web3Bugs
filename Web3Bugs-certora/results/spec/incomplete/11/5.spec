// Source: contracts/11/specs/fullyBackedBonding.spec
// Property: totalAssetsPreserved (original lines 215-225)
// Original CVL dependency source lines: 14,23,25,26,27,28;43;46;50-53;70-73;85-91;215-225
// Dependency status: incomplete; historical source syntax kept unchanged.

methods {
    init_state() envfree
    seizeBond(address, uint, uint, address)
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

rule totalAssetsPreserved(address operator, address owner, address beneficiary,  method f) {
    env e;
    calldataarg args;
    mathint totalAssetsBefore = totalLockedBonds(operator) + unbondedValue(operator);
    require f.selector != seizeBond(address,uint256,uint256,address).selector &&
             f.selector != withdraw(uint256,address).selector;
    f(e, args);
    mathint totalAssetsAfter = totalLockedBonds(operator) + unbondedValue(operator);
    assert totalAssetsAfter == totalAssetsBefore ||  totalAssetsAfter == totalAssetsBefore + e.msg.value,
    "$f can change the total assets of an operator in an unexpected way";
}
