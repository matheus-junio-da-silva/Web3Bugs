// Project 23 exact historical source: Splits.spec
// Property assetsDoNotInterfereEachOther original lines 216-260 SHA256 fd33e4dfbd9de0475563058b315372ba994e148effe8b878eaf4b58ad6927f84
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

rule assetsDoNotInterfereEachOther() {
    env e; uint256 assetId1; uint256 assetId2; uint256 userA_Id; uint256 userB_Id;

    // make sure the users/assets are not the same
    require userA_Id != userB_Id;
    require assetId1 != assetId2;

    // recording the state before split()
    uint128 userA_splittableAssetId1_Before = splittable(e, userA_Id, assetId1);
    uint128 userA_collectableAssetId1_Before = collectable(e, userA_Id, assetId1);
    uint128 userA_splittableAssetId2_Before = splittable(e, userA_Id, assetId2);
    uint128 userA_collectableAssetId2_Before = collectable(e, userA_Id, assetId2);

    uint128 userB_splittableAssetId1_Before = splittable(e, userB_Id, assetId1);
    uint128 userB_collectableAssetId1_Before = collectable(e, userB_Id, assetId1);
    uint128 userB_splittableAssetId2_Before = splittable(e, userB_Id, assetId2);
    uint128 userB_collectableAssetId2_Before = collectable(e, userB_Id, assetId2);

    // calling the split() for userA over assertId1
    uint128 userA_collectableAmtAssetId1; uint128 userA_splitAmtAssetId1;
    userA_collectableAmtAssetId1, userA_splitAmtAssetId1 = split(e, userA_Id, assetId1, true);

    // recording the state after split()
    uint128 userA_splittableAssetId1_After = splittable(e, userA_Id, assetId1);
    uint128 userA_collectableAssetId1_After = collectable(e, userA_Id, assetId1);
    uint128 userA_splittableAssetId2_After = splittable(e, userA_Id, assetId2);
    uint128 userA_collectableAssetId2_After = collectable(e, userA_Id, assetId2);

    uint128 userB_splittableAssetId1_After = splittable(e, userB_Id, assetId1);
    uint128 userB_collectableAssetId1_After = collectable(e, userB_Id, assetId1);
    uint128 userB_splittableAssetId2_After = splittable(e, userB_Id, assetId2);
    uint128 userB_collectableAssetId2_After = collectable(e, userB_Id, assetId2);

    // the expectation:
    // splittable and collectable for any user's assetId2 stays the same
    assert userA_splittableAssetId2_After == userA_splittableAssetId2_Before;
    assert userA_collectableAssetId2_After == userA_collectableAssetId2_Before;

    assert userB_splittableAssetId2_After == userB_splittableAssetId2_Before;
    assert userB_collectableAssetId2_After == userB_collectableAssetId2_Before;
    // the collectable of userB's assetId1 should not be affected by the split
    assert userB_collectableAssetId1_After == userB_collectableAssetId1_Before;
    // the splittable of userB's assetId1 should not decrease
    assert userB_splittableAssetId1_After >= userB_splittableAssetId1_Before;
}
