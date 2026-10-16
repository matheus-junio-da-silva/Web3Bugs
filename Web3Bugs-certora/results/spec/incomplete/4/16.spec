// Extracted from Project 4 — AAVE Staked Token v1.5
// Property: returnFundsDecreaseExchangeRate
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope.
// Included original CVL ranges: certora/specs/base.spec:4-4; certora/specs/base.spec:11-11; certora/specs/base.spec:22-22; certora/specs/base.spec:44-44; certora/specs/base.spec:48-48; certora/specs/invariants.spec:27-29; certora/specs/allProps.spec:499-511

methods {
    LOWER_BOUND() returns (uint256) envfree
    getExchangeRate() returns (uint216) envfree
    returnFunds(uint256)
}
invariant lowerBoundNotZero()
    LOWER_BOUND() > 0
rule returnFundsDecreaseExchangeRate(address receiver, uint256 amount) {
    env e;
    uint216 _ExchangeRate = getExchangeRate();

    // Currently, in the constructor, LOWER_BOUND = 10**decimals
    requireInvariant lowerBoundNotZero();

    returnFunds(e, amount);

    uint216 ExchangeRate_ = getExchangeRate();

    assert ExchangeRate_ <= _ExchangeRate;
}
