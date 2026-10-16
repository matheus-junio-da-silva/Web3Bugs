// Extracted from Project 4 — AAVE Staked Token v1.5
// Property: airdropNotMutualized
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope.
// Included original CVL ranges: certora/specs/base.spec:1-1; certora/specs/base.spec:4-4; certora/specs/base.spec:22-22; certora/specs/base.spec:48-48; certora/specs/allProps.spec:242-248

using DummyERC20Impl as stake_token
methods {
    getExchangeRate() returns (uint216) envfree
}
rule airdropNotMutualized(uint256 amount){
    env e;
    uint216 exchangeRateBefore = getExchangeRate();
    stake_token.transfer(e, currentContract, amount);
    uint216 exchangeRateAfter = getExchangeRate();
    assert exchangeRateBefore == exchangeRateAfter;
}
