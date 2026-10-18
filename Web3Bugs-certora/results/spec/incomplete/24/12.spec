// Project 24 source contracts/24/spec/LEInProgress.spec lines 25-55; original CVL syntax, no CVL2 migration.
// Original prerequisite CVL declarations from LEInProgress.spec
// STATUS - in progress



// Verbatim active rule follows
rule hl_moreDepositMoreGet(method f, env e, env e2, env e3, env e4, env e5){
    require e.msg.sender != e2.msg.sender;
    require e.msg.sender != e3.msg.sender;
    require e2.msg.sender != e3.msg.sender;
    require e.msg.sender != issuer();
    require e2.msg.sender != issuer();
    require e.msg.sender != currentContract;
    require e2.msg.sender != currentContract;
    require e3.msg.sender != currentContract;
    require e.msg.value > e2.msg.value;
    require e.msg.sender == e4.msg.sender;  // need two more envs because depositAVAX() is payble but pairBalance() and getIncentives() aren't thus need the same addresses but different e.msg.value == 0 and != 0
    require e2.msg.sender == e5.msg.sender;
    require !userHasWithdrawnIncentives(e.msg.sender);
    require !userHasWithdrawnIncentives(e2.msg.sender);

    require open();

    depositAVAX(e);
    depositAVAX(e2);

    createPair(e3);

    uint256 incentivesBalanceOne = getIncentives(e4, e4.msg.sender);
    uint256 incentivesBalanceTwo = getIncentives(e5, e5.msg.sender);

    uint256 pairBalanceOne = pairBalance(e4, e4.msg.sender);
    uint256 pairBalanceTwo = pairBalance(e5, e5.msg.sender);
    
    assert exists uint256 dt. e.msg.value - e2.msg.value > dt => incentivesBalanceOne > incentivesBalanceTwo;
    // assert exists uint256 dt. e.msg.value - e2.msg.value > dt => pairBalanceOne > pairBalanceTwo;
}
