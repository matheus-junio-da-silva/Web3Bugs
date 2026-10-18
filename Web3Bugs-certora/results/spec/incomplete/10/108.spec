// Project 10 — literal active noOtherPartyModified from contracts/10/specs/proxy.spec:534-550
// CVL dependencies selected by transitive reference; historical CVL syntax is not migrated.
// Snapshot is not an executable proof of the 2021 audit.


using DummyERC20A as someToken
using DummyERC20B as someToken2
using Summary as summaryInstance // general summary for DeFi protocols

methods {
    someToken.balanceOf(address) returns (uint) envfree
    someToken2.balanceOf(address) returns (uint) envfree
}

rule noOtherPartyModified(method f, address somebody) {
    require somebody != currentContract;
    require somebody != summaryInstance;
    require somebody != 0; // 0 is reserved for minting/burning so we exclude it.

    uint origTokenABalance = someToken.balanceOf(somebody);
    uint origTokenBBalance = someToken2.balanceOf(somebody);

    env e;
    require e.msg.sender != 0; // 0 is reserved for minting/burning so we exclude it.
    require e.msg.sender != summaryInstance; // presumably, the DeFi protocol cannot invoke itself (Flashloan risk!)
    calldataarg arg;
    f(e, arg);

    assert someToken.balanceOf(somebody) == origTokenABalance 
        && someToken2.balanceOf(somebody) == origTokenBBalance;
}
