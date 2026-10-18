// Project 23 exact historical source: Splits.spec
// Property sameReturnOfSplitAndSplitResults original lines 311-347 SHA256 fd33e4dfbd9de0475563058b315372ba994e148effe8b878eaf4b58ad6927f84
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

rule sameReturnOfSplitAndSplitResults() {
    env e; uint256 assetId; uint256 userA_Id; uint256 userB_Id; uint256 userC_Id;
    require userA_Id != userB_Id;   require userA_Id != userC_Id;   require userB_Id != userC_Id;

    // setting up the currReceivers[] of userA
    uint256 length = getCurrSplitsReceiverLocaLength(e, true);
    uint256 index1; uint256 userId1; uint32 weight1;
    uint256 index2; uint256 userId2; uint32 weight2;

    userId1, weight1 = getCurrSplitsReceiverLocalArr(e, true, index1);
    userId2, weight2 = getCurrSplitsReceiverLocalArr(e, true, index2);

    require length == 2;
    require index1 != index2;
    require userId1 == userB_Id;
    require userId2 == userC_Id;
    require weight1 > 0;
    require weight2 > 0;
    require weight1 + weight2 <= 1000000;  // safe assumptions
    // safe assumptions since the function _assertSplitsValid()
    // verified that totalWeight <= _TOTAL_SPLITS_WEIGHT upon _setSplits()
    // we force the receivers to be only two, therefore totalWeight = weight1 + weight2
    // _TOTAL_SPLITS_WEIGHT == 1000000, hence the assumption above is safe

    // calling splitResults() upon userA with amount = userA.splittable
    uint128 userA_splittableBefore = splittable(e, userA_Id, assetId);
    uint128 userA_splitAmt_splitResults; uint128 userA_collectableAmt_splitResults;
    userA_collectableAmt_splitResults, userA_splitAmt_splitResults = splitResults(e, userA_Id, true, userA_splittableBefore);
    
    // calling split() on userA
    uint128 userA_collectableAmt_split; uint128 userA_splitAmt_split;
    userA_collectableAmt_split, userA_splitAmt_split = split(e, userA_Id, assetId, true);

    // the expectation:
    assert userA_collectableAmt_split == userA_collectableAmt_splitResults;
    assert userA_splitAmt_split == userA_splitAmt_splitResults;
}
