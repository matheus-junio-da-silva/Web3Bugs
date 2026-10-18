// Project 24 source contracts/24/spec/LEInProgress.spec lines 2-19; original CVL syntax, no CVL2 migration.
// Original prerequisite CVL declarations from LEInProgress.spec
// STATUS - in progress



// Verbatim active rule follows
rule transition_balThisZero(address user, method f, env e) {
    safeAssumptions(e);
    require currentPhase(e) == PhaseThree();

    uint256 wavaxBalanceBefore = getWAVAXbalanceOfThis();
    uint256 wavaxPairBalanceBefore = getWAVAXbalanceOfPair();
    uint256 avaxAllocBefore = avaxAllocated();

    require open();
    calldataarg args;
    createPair(e);
    require closed();

    uint256 wavaxBalanceAfter = getWAVAXbalanceOfThis();

    assert wavaxBalanceBefore == wavaxBalanceAfter, "wavax balance of LE contract was changed";
    assert getWAVAXbalanceOfPair() - wavaxPairBalanceBefore == avaxAllocated(), "correlation is wrong";
}
