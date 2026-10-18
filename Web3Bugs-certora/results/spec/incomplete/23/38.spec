// Project 23 exact historical source: Splits.spec
// Property cannotFrontRunSplitGeneralCase original lines 477-523 SHA256 fd33e4dfbd9de0475563058b315372ba994e148effe8b878eaf4b58ad6927f84
//// ## Verification of Splits.sol
//// 
//// `Splits.sol` is part of the Drips protocol
//// 
//// The splits functionality, as explained in DripsHub.sol by the developers:
//// The user can share collected funds with other users by using splits.
//// When collecting, the user gives each of their splits receivers a fraction of the received funds.
//// Funds received from splits are available for collection immediately regardless of the cycle.
//// They aren't exempt from being split, so they too can be split when collected.
//// Users can build chains and networks of splits between each other.
//// Anybody can request collection of funds for any user,
//// which can be used to enforce the flow of funds in the network of splits.
//// 
//// ### Assumptions and Simplifications
//// - All the internal methods are wrapped in CVT callable versions
//// - Dummy functions used to control the SplitsReceiver[] receivers
//// - When testing the split weight functionality we safely assumed weight < _TOTAL_SPLITS_WEIGHT
////   since the method _assertSplitsValid() validates them before assignment
//// 
//// ### Properties


/// @notice Calculate results of splitting an amount using the current splits configuration.
/// We verify that amount == collectableAmt + splitAmt
/// Since compiling with Solidity >0.8.0 there are no overflows

rule cannotFrontRunSplitGeneralCase() {
    env e; env e2; uint256 assetId; uint256 userA_Id; uint256 userB_Id; uint256 userC_Id;
    uint128 userA_collectableAmt; uint128 userA_splitAmt;
    uint128 userA_collectableAmt2; uint128 userA_splitAmt2;
    uint128 userB_collectableAmt; uint128 userB_splitAmt;
    uint128 userA_splittableBefore = splittable(e, userA_Id, assetId);
    uint128 userB_splittableBefore = splittable(e, userB_Id, assetId);
    uint128 userC_splittableBefore = splittable(e, userC_Id, assetId);
    uint128 userA_collectableBefore = collectable(e, userA_Id, assetId);
    uint128 userB_collectableBefore = collectable(e, userB_Id, assetId);
    uint128 userC_collectableBefore = collectable(e, userC_Id, assetId);

    // prevents overflow of the splittable of the receiver userC:
    require userA_splittableBefore + userB_splittableBefore + userC_splittableBefore < 2^128;
    // prevents overflow of the collectable of the splitters userA and userB:
    require userA_collectableBefore + userA_splittableBefore < 2^128;
    require userB_collectableBefore + userB_splittableBefore < 2^128;
    // prevents overflow in the edge cases of (userC == userA) or (userC == userB):
    require userA_collectableBefore + userA_splittableBefore + userB_splittableBefore < 2^128;
    require userB_collectableBefore + userB_splittableBefore + userA_splittableBefore < 2^128;
    
    // setting up the currReceivers[] of userA and userB to be the same - singe receiver userC
    uint256 length1 = getCurrSplitsReceiverLocaLength(e, true);
    require length1 == 1;  // only one receiver
    uint256 index1; uint256 userId1; uint32 weight1;
    userId1, weight1 = getCurrSplitsReceiverLocalArr(e, true, index1);

    require userId1 == userC_Id;
    require weight1 <= 1000000;  // safe assumption
    require weight1 > 0;  // safe assumption
    // safe assumptions since the function _assertSplitsValid()
    // verified that totalWeight <= _TOTAL_SPLITS_WEIGHT upon _setSplits()
    // we required that there is only one receiver, therefore totalWeight = weight1
    // _TOTAL_SPLITS_WEIGHT == 1000000, hence the assumption above is safe
    // also _assertSplitsValid() verified that weight != 0

    storage initStorage = lastStorage;

    userA_collectableAmt, userA_splitAmt = split(e, userA_Id, assetId, true);
    uint128 userC_splittableAfterSplitA = splittable(e, userC_Id, assetId);
    
    userB_collectableAmt, userB_splitAmt = split(e, userB_Id, assetId, true) at initStorage;
    uint128 userC_splittableAfterSplitB = splittable(e, userC_Id, assetId);

    userA_collectableAmt2, userA_splitAmt2 = split@withrevert(e, userA_Id, assetId, true);
    assert !lastReverted;
}
