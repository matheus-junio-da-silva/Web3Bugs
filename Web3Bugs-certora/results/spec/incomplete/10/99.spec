// Project 10 — literal active tokenMovementCorrectness from contracts/10/specs/proxy.spec:509-532
// CVL dependencies selected by transitive reference; historical CVL syntax is not migrated.
// Snapshot is not an executable proof of the 2021 audit.


using Summary as summaryInstance // general summary for DeFi protocols

methods {
    summaryInstance.consumedToken() returns (address) envfree
    summaryInstance.generatedToken() returns (address) envfree
    summaryInstance.shouldBeConsumedAmount() returns (uint) envfree
    summaryInstance.getBalance(address,address) returns (uint) envfree
    summaryInstance.erc20A() returns (address) envfree
    summaryInstance.erc20B() returns (address) envfree
}

rule tokenMovementCorrectness(method f) {
    storage initialStorage = lastStorage;
    require summaryInstance.consumedToken() == 0;
    require summaryInstance.generatedToken() == 0;
    require summaryInstance.erc20A() != summaryInstance.erc20B();
    
    env e;
    require e.msg.sender != 0; // 0 is reserved for minting/burning so we exclude it.
    require e.msg.sender != summaryInstance; // presumably, the DeFi protocol cannot invoke itself (Flashloan risk!)
    calldataarg arg;
    f(e, arg);

    address consumed = summaryInstance.consumedToken();
    address generated = summaryInstance.generatedToken();
    uint updatedConsumedTokenBalance = summaryInstance.getBalance(consumed, currentContract);
    uint updatedGeneratedTokenBalance = summaryInstance.getBalance(generated, currentContract);
    uint expectedConsumedAmount = summaryInstance.shouldBeConsumedAmount();
    uint origConsumedTokenBalance = summaryInstance.getBalance(consumed, currentContract) at initialStorage;
    uint origGeneratedTokenBalance = summaryInstance.getBalance(generated, currentContract);

    assert consumed != 0 => updatedConsumedTokenBalance == origConsumedTokenBalance - expectedConsumedAmount, "If there is a consumed token, should have consumed exactly the amount";
    assert (expectedConsumedAmount > 0 && generated != 0) => updatedGeneratedTokenBalance > origGeneratedTokenBalance, 
        "If consumed positive amount and expected to generate an amount, then should have generated a positive amount";
}
