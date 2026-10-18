// Project 14 — Opyn Gamma Protocol; historical CVL (not CVL2)
// Literal active declaration: specs/controller.spec:135-152
// Minimal explicit CVL declaration closure; model-wide ABI/implicit selector dependencies are in the historical target and scripts.
using MarginPoolHarness as pool

using Whitelist as whitelist

using OtokenHarnessB as longOtoken

methods {
    longOtoken.balanceOf(address) returns uint256 envfree
    whitelist.isWhitelistedCollateral(address) returns bool envfree
}

rule optionWithdrawsRestricted(address owner, uint256 vaultId, uint256 index, address from, address amount, method f) {
    env e;
    // The pool cannot really call any of these functions
    require (e.msg.sender != pool);
    require (!whitelist.isWhitelistedCollateral(longOtoken));
    uint256 otokenBalanceBefore = longOtoken.balanceOf(pool);
    if (f.selector == burnOtokenB(address,uint256,address,uint256,uint256).selector) {
        require(owner != pool);
        sinvoke burnOtokenB(e, owner, vaultId, from, index, amount);
    } else {
        calldataarg arg;
        sinvoke f(e, arg);
    }
    uint256 otokenBalanceAfter = longOtoken.balanceOf(pool);
    // or settle vault 
    assert otokenBalanceAfter < otokenBalanceBefore => (f.selector == withdrawLongB(address, uint256, address, uint256, uint256).selector) 
                                                    || (f.selector == settleVault(address,uint256,address).selector);
}
