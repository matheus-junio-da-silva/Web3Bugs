// Project 10 — literal active transferredTokensMeanThatStackIsUpdated from contracts/10/specs/proxy.spec:476-491
// CVL dependencies selected by transitive reference; historical CVL syntax is not migrated.
// Snapshot is not an executable proof of the 2021 audit.


using DummyERC20A as someToken
using ProxyHarness as proxy // may also be the same as currentContract
using Summary as summaryInstance // general summary for DeFi protocols

methods {
    getStackLength() returns (uint256) envfree
    someToken.balanceOf(address) returns (uint) envfree
    someToken.allowance(address,address) returns (uint) envfree
    summaryInstance.getEthAddress(address) returns (address) envfree
}

definition MAX_UINT256() returns uint256 = 115792089237316195423570985008687907853269984665640564039457584007913129639935
    ;

definition STACK_INCREASE_BOUND() returns uint256 = 1000000 ;    // 1 million

function arbitrary(method f) {
    env e__;
    calldataarg arg__;
    f(e__, arg__);
}

rule transferredTokensMeanThatStackIsUpdated(method f) {
    require summaryInstance.getEthAddress(currentContract) != someToken; // not an eth transfer
    require someToken != 0; // not an eth transfer
    require someToken.allowance(currentContract, summaryInstance) == 0; // to make sure we're starting clean as implied by approvedTokensAreTemporary
    uint256 balanceBefore = someToken.balanceOf(currentContract);
    uint256 stackLengthBefore = getStackLength();
    require stackLengthBefore < MAX_UINT256() - STACK_INCREASE_BOUND(); // see stackLengthIncreaseIsBounded
    
    arbitrary(f);

    uint256 balanceAfter = someToken.balanceOf(currentContract);
    uint256 stackLengthAfter = getStackLength();
    
    assert (balanceAfter > balanceBefore) => stackLengthAfter > stackLengthBefore, 
        "must push an entry to postprocess stack if transferring funds into proxy which are not eth";
}
