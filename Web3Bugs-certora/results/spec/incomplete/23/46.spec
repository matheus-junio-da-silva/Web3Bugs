// Project 23 exact historical source: Splits2.spec
// Property revertCharacteristicsOfSplit original lines 211-235 SHA256 3b7e364bb8dcaed31c99941375dca0df633b36d56f8d91528c1f80239e189ea1
/// @notice front running split() does not affect receiver
/// userA has a single splitReceiver userC
/// userB also has the same single splitReceiver UserC
/// we want to verify split() can be called on userA successfully
/// even if someone front runs it and calls splits() first on userB
/// no assumptions about userA, userB, userC

rule revertCharacteristicsOfSplit() {
    env e; uint256 userA_Id; uint256 assetId;
    uint128 userA_collectableAmt; uint128 userA_splitAmt;

    // allowing only valid splitReceivers because revert is not allowed
    bytes32 receiversHash = hashSplits(e, true);
    assertSplitsValid(e, true, receiversHash);
    setSplits(e, userA_Id, true);

    uint128 userA_splittableBefore = splittable(e, userA_Id, assetId);
    uint128 userA_collectableBefore = collectable(e, userA_Id, assetId);

    require userA_splittableBefore + userA_collectableBefore < 2^128;

    userA_collectableAmt, userA_splitAmt = split(e, userA_Id, assetId, true);

    uint128 userA_splittableAfter = splittable(e, userA_Id, assetId);
    uint128 userA_collectableAfter = collectable(e, userA_Id, assetId);

    //require userA_splittableAfter + userA_collectableAfter < 2^128;

    userA_collectableAmt, userA_splitAmt = split@withrevert(e, userA_Id, assetId, true);

    assert !lastReverted;
}
