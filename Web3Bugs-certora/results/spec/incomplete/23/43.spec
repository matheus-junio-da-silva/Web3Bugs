// Project 23 exact historical source: Splits2.spec
// Property cannotFrontRunSplitDifferentUsers original lines 62-112 SHA256 3b7e364bb8dcaed31c99941375dca0df633b36d56f8d91528c1f80239e189ea1
/// @notice front running split() does not affect receiver
/// userA has a single splitReceiver userC
/// userB also has the same single splitReceiver UserC
/// we want to verify split() can be called on userA successfully
/// even if someone front runs it and calls splits() first on userB
/// no assumptions about userA, userB, userC

rule cannotFrontRunSplitDifferentUsers() {
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

    require userA_Id != userB_Id;
    require userA_Id != userC_Id;
    require userB_Id != userC_Id;

    // prevents overflow of the splittable of the receiver userC:
    require userA_splittableBefore + userB_splittableBefore + userC_splittableBefore < 2^128;
    // prevents overflow of the collectable of the splitters userA and userB:
    //require userA_collectableBefore + userA_splittableBefore < 2^128;
    //require userB_collectableBefore + userB_splittableBefore < 2^128;
    // prevents overflow in the edge cases of (userC == userA) or (userC == userB):
    //require userA_collectableBefore + userA_splittableBefore + userB_splittableBefore < 2^128;
    //require userB_collectableBefore + userB_splittableBefore + userA_splittableBefore < 2^128;
    
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
