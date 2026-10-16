// Extracted from Project 4 — AAVE Staked Token v1.5
// Property: slashAndReturnFundsOfZeroDoesntChangeExchangeRate
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope.
// Included original CVL ranges: certora/specs/base.spec:4-4; certora/specs/base.spec:22-22; certora/specs/base.spec:43-43; certora/specs/base.spec:44-44; certora/specs/base.spec:48-48; certora/specs/allProps.spec:561-575

methods {
    getExchangeRate() returns (uint216) envfree
    slash(address,uint256) returns (uint256)
    returnFunds(uint256)
}
rule slashAndReturnFundsOfZeroDoesntChangeExchangeRate() {
    env e;
    address dest; uint256 amt = 0;
    uint216 _ER = getExchangeRate();
    storage initialStorage = lastStorage;

    slash(e, dest, amt);
    uint216 ER_AfterSlash = getExchangeRate();

    returnFunds(e, amt) at initialStorage;
    uint216 ER_AfterReturnFunds = getExchangeRate();

    assert(ER_AfterSlash == ER_AfterReturnFunds);
    assert(ER_AfterReturnFunds == _ER);
}
