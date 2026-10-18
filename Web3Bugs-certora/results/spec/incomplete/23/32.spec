// Project 23 exact historical source: Splits.spec
// Property integrityOfSplit original lines 143-209 SHA256 fd33e4dfbd9de0475563058b315372ba994e148effe8b878eaf4b58ad6927f84
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

rule integrityOfSplit() {
    env e; uint256 assetId;
    uint256 userA_Id; uint256 userB_Id; uint256 userC_Id; uint256 userD_Id;
    
    require userA_Id != userB_Id;   require userA_Id != userD_Id;
    require userA_Id != userC_Id;   require userB_Id != userD_Id;
    require userB_Id != userC_Id;   require userC_Id != userD_Id;

    // obtaining splittable/collectable states before calling split()
    uint128 userA_splittableBefore = splittable(e, userA_Id, assetId);
    require userA_splittableBefore > 0;
    uint128 userA_collectableBefore = collectable(e, userA_Id, assetId);
    uint128 userB_splittableBefore = splittable(e, userB_Id, assetId);
    uint128 userB_collectableBefore = collectable(e, userB_Id, assetId);
    uint128 userC_splittableBefore = splittable(e, userC_Id, assetId);
    uint128 userC_collectableBefore = collectable(e, userC_Id, assetId);
    uint128 userD_splittableBefore = splittable(e, userD_Id, assetId);
    uint128 userD_collectableBefore = collectable(e, userD_Id, assetId);

    // setting up the currReceivers[] of userA
    uint256 index1; uint256 userId1; uint32 weight1;
    uint256 index2; uint256 userId2; uint32 weight2;
    userId1, weight1 = getCurrSplitsReceiverLocalArr(e, true, index1);
    userId2, weight2 = getCurrSplitsReceiverLocalArr(e, true, index2);

    require index1 != index2;     // different indexes sample different splitReceivers
    require userId1 == userB_Id;  // userB is on the list of splitReceivers of userA
    require userId2 != userC_Id;  // the second splitReceiver is not userC
    require userId2 != userA_Id;  // the second splitReceiver is not the splitter itself
    require userId2 == userD_Id;  // since we run with loop_iter 2, there are max 2 receivers

    // calling the split() on userA
    uint128 userA_collectableAmt;   uint128 userA_splitAmt;
    userA_collectableAmt, userA_splitAmt = split(e, userA_Id, assetId, true);

    // obtaining splittable/collectable states after calling split()
    uint128 userA_splittableAfter = splittable(e, userA_Id, assetId);
    uint128 userA_collectableAfter = collectable(e, userA_Id, assetId);
    uint128 userB_splittableAfter = splittable(e, userB_Id, assetId);
    uint128 userB_collectableAfter = collectable(e, userB_Id, assetId);
    uint128 userC_splittableAfter = splittable(e, userC_Id, assetId);
    uint128 userC_collectableAfter = collectable(e, userC_Id, assetId);
    uint128 userD_splittableAfter = splittable(e, userD_Id, assetId);
    uint128 userD_collectableAfter = collectable(e, userD_Id, assetId);


    // the expectation:
    // UserA's splittable should NOT increase
    assert userA_splittableAfter <= userA_splittableBefore;
    assert userA_splittableAfter == 0; // it should be zero

    // UserB is on the list of UserA's splitters, therefore "userB's splittable should NOT decrease"
    assert userB_splittableAfter >= userB_splittableBefore;

    // UserC is NOT on the list of UserA's splitters, therefore "userC's splittable should NOT change"
    assert userC_splittableAfter == userC_splittableBefore;

    // UserA's collectable should NOT decrease, UserB and UserC's collectable should NOT change
    assert userA_collectableAfter >= userA_collectableBefore;
    assert userB_collectableAfter == userB_collectableBefore;
    assert userC_collectableAfter == userC_collectableBefore;

    // The increase of the splittable of the receivers userB and userD should be equal the splittable of userA
    assert (userB_splittableAfter - userB_splittableBefore) +
           (userD_splittableAfter - userD_splittableBefore) +
           (userA_collectableAfter - userA_collectableBefore) == userA_splittableBefore;
}
