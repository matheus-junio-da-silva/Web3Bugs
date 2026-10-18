// Project 23 exact historical source: Splits.spec
// Property equalSplitWeightsResultEqualSplittableIncrease original lines 413-456 SHA256 fd33e4dfbd9de0475563058b315372ba994e148effe8b878eaf4b58ad6927f84
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

rule equalSplitWeightsResultEqualSplittableIncrease() {
    env e; uint256 assetId; uint256 userA_Id; uint256 userB_Id; uint256 userC_Id;


    // all the 3 users are different
    require userA_Id != userB_Id; require userA_Id != userC_Id; require userB_Id != userC_Id;


    // setting up the currReceivers[] of userA
    uint256 index1; uint256 userId1; uint32 weight1; uint256 index2; uint256 userId2; uint32 weight2;
    userId1, weight1 = getCurrSplitsReceiverLocalArr(e, true, index1);
    userId2, weight2 = getCurrSplitsReceiverLocalArr(e, true, index2);
    uint256 length = getCurrSplitsReceiverLocaLength(e, true);

    require length == 2;            // only two split receivers
    require index1 != index2;       // different indexes sample different splitReceivers
    require userId1 == userB_Id;
    require userId2 == userC_Id;
    require weight1 == weight2;
    require weight1 <= 500000;      // safe assumption since MAX _TOTAL_SPLITS_WEIGHT == 1000000
    require weight1 > 0;            // safe assumption

    uint128 userA_splittableBefore = splittable(e, userA_Id, assetId); 
    uint128 userB_splittableBefore = splittable(e, userB_Id, assetId);
    uint128 userC_splittableBefore = splittable(e, userC_Id, assetId);
    require userA_splittableBefore > 0; // there is a splittable amount to be split

    // calling the split() on userA
    uint128 userA_collectableAmt;   uint128 userA_splitAmt;
    userA_collectableAmt, userA_splitAmt = split(e, userA_Id, assetId, true);

    uint128 userA_splittableAfter = splittable(e, userA_Id, assetId);
    uint128 userB_splittableAfter = splittable(e, userB_Id, assetId);
    uint128 userC_splittableAfter = splittable(e, userC_Id, assetId);

    // the expectation:
    // the splittable balances of userB and userC will increase by the same amount
    // in case of rounding - diffrence between amounts can be 1
    uint128 userB_splittableChange = userB_splittableAfter - userB_splittableBefore;
    uint128 userC_splittableChange = userC_splittableAfter - userC_splittableBefore;
    assert ((userC_splittableChange == userB_splittableChange) || 
            (userB_splittableChange == userC_splittableChange + 1) || 
            (userC_splittableChange == userB_splittableChange + 1));    
}
