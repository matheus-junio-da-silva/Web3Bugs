// Extracted from Project 4 — AAVE Staked Token v1.5
// Property: integrityOfRedeem
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope.
// Included original CVL ranges: certora/specs/base.spec:1-1; certora/specs/base.spec:4-4; certora/specs/base.spec:6-6; certora/specs/base.spec:15-15; certora/specs/base.spec:16-16; certora/specs/base.spec:28-28; certora/specs/base.spec:42-42; certora/specs/base.spec:48-48; certora/specs/allProps.spec:597-609

using DummyERC20Impl as stake_token
methods {
    stake_token.balanceOf(address) returns (uint256) envfree
    balanceOf(address) returns (uint256) envfree
    cooldownAmount(address) returns (uint216) envfree
    previewRedeem(uint256) returns (uint256) envfree
    redeem(address,uint256)
}
rule integrityOfRedeem(method f, env e, address to, uint256 amount) {
    require balanceOf(e.msg.sender) >= amount;
    require currentContract != to;
    uint256 totalUnderlying = previewRedeem(amount);
    uint256 _receiverBalance = stake_token.balanceOf(to);

    redeem(e, to, amount);

    uint256 receiverBalance_ = stake_token.balanceOf(to);

    assert(amount <= cooldownAmount(e.msg.sender) =>
        totalUnderlying == receiverBalance_ - _receiverBalance);
}
