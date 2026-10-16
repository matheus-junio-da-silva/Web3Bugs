// Extracted from Project 4 — AAVE Staked Token v1.5
// Property: slashingIncreaseExchangeRate
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope.
// Included original CVL ranges: certora/specs/base.spec:4-4; certora/specs/base.spec:22-22; certora/specs/base.spec:43-43; certora/specs/base.spec:48-48; certora/specs/allProps.spec:471-481

methods {
    getExchangeRate() returns (uint216) envfree
    slash(address,uint256) returns (uint256)
}
rule slashingIncreaseExchangeRate(address receiver, uint256 amount) {
    env e; calldataarg args;

    uint216 _ExchangeRate = getExchangeRate();

    slash(e, args);

    uint216 ExchangeRate_ = getExchangeRate();

    assert ExchangeRate_ >= _ExchangeRate;
}
