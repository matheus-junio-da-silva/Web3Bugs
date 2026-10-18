// Project 23 exact historical source: Splits.spec
// Property moneyNotLostOrCreatedDuringSplit original lines 268-303 SHA256 fd33e4dfbd9de0475563058b315372ba994e148effe8b878eaf4b58ad6927f84
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

rule moneyNotLostOrCreatedDuringSplit() {
    env e; uint256 assetId;
    uint256 userA_Id; uint256 userB_Id;

    // setting up the currReceivers[] of userA
    uint256 length; uint256 index1; uint256 userId1; uint32 weight1;
    userId1, weight1 = getCurrSplitsReceiverLocalArr(e, true, index1);
    length = getCurrSplitsReceiverLocaLength(e, true);
    require length == 1;            // only one splitsReceiver
    require userId1 == userB_Id;    // making sure it is userB (not limiting it to be userA)
    require weight1 <= 1000000;     // safe assumptions since the function _assertSplitsValid()
                                    // verified that totalWeight <= _TOTAL_SPLITS_WEIGHT upon _setSplits()
                                    // we required that there is only one receiver, therefore totalWeight = weight1
                                    // _TOTAL_SPLITS_WEIGHT == 1000000, hence the assumption above is safe

    // recording the state before split()
    uint128 userA_splittableBefore = splittable(e, userA_Id, assetId);
    uint128 userA_collectableBefore = collectable(e, userA_Id, assetId);
    uint128 userB_splittableBefore = splittable(e, userB_Id, assetId);
    uint128 userB_collectableBefore = collectable(e, userB_Id, assetId);

    // calling the split() on userA
    uint128 userA_collectableAmt;   uint128 userA_splitAmt;
    userA_collectableAmt, userA_splitAmt = split(e, userA_Id, assetId, true);

    // recording the state after split()
    uint128 userA_splittableAfter = splittable(e, userA_Id, assetId);
    uint128 userA_collectableAfter = collectable(e, userA_Id, assetId);
    uint128 userB_splittableAfter = splittable(e, userB_Id, assetId);
    uint128 userB_collectableAfter = collectable(e, userB_Id, assetId);

    // the expectation:
    uint128 moneyBefore = userA_splittableBefore + userA_collectableBefore + userB_splittableBefore + userB_collectableBefore;
    uint128 moneyAfter = userA_splittableAfter + userA_collectableAfter + userB_splittableAfter + userB_collectableAfter;
    assert moneyBefore == moneyAfter;
}
