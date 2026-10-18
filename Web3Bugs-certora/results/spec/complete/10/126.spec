// Project 10 — literal active approvedTokensAreTemporary from contracts/10/specs/proxy.spec:493-504
// CVL dependencies selected by transitive reference; historical CVL syntax is not migrated.
// Snapshot is not an executable proof of the 2021 audit.


using DummyERC20A as someToken
using Summary as summaryInstance // general summary for DeFi protocols

methods {
    someToken.allowance(address,address) returns (uint) envfree
    summaryInstance.getEthAddress(address) returns (address) envfree
}

function arbitrary(method f) {
    env e__;
    calldataarg arg__;
    f(e__, arg__);
}

rule approvedTokensAreTemporary(method f, address someAllowed) {
    require summaryInstance.getEthAddress(currentContract) != someToken; // not an eth transfer
    require someToken != 0; // not an eth transfer
    require someAllowed == summaryInstance; // narrowing down
    uint256 allowanceBefore = someToken.allowance(currentContract, someAllowed);

    arbitrary(f);
    
    uint256 allowanceAfter = someToken.allowance(currentContract, someAllowed);

    assert allowanceBefore == 0 => allowanceAfter == 0, "Allowances must be nullified";
}
