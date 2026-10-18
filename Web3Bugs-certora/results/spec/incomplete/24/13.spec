// Project 24 source contracts/24/spec/LEInProgress.spec lines 60-73; original CVL syntax, no CVL2 migration.
// Original prerequisite CVL declarations from LEInProgress.spec
// STATUS - in progress



// Verbatim active rule follows
rule hl_withdrawLateMorePenalty(method f, env e, env e2){
    require auctionStart() < e.block.timestamp;
    require e.block.timestamp < e2.block.timestamp;
    require phaseOneNoFeeDuration() == oneDay();
    require phaseOneDuration() == twoDays();
    require e.block.timestamp > auctionStart() + phaseOneNoFeeDuration();
    require e.block.timestamp < auctionStart() + phaseOneDuration();
    require e2.block.timestamp < auctionStart() + phaseOneDuration();

    uint256 earlyPenalty = getPenalty(e);
    uint256 latePenalty = getPenalty(e2);

    assert exists uint256 dt. e2.block.timestamp - e.block.timestamp > dt => latePenalty > earlyPenalty;
}
