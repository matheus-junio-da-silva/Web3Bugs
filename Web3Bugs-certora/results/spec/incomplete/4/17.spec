// Extracted from Project 4 — AAVE Staked Token v1.5
// Property: exchangeRateNeverZero
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope.
// Included original CVL ranges: certora/specs/base.spec:4-4; certora/specs/base.spec:22-22; certora/specs/base.spec:48-48; certora/specs/allProps.spec:533-543

methods {
    getExchangeRate() returns (uint216) envfree
}
rule exchangeRateNeverZero(method f) {
    env e; calldataarg args;
    uint216 _ER = getExchangeRate();
    require _ER != 0;

    f(e, args);

    uint216 ER_ = getExchangeRate();

    assert ER_ != 0;
}
