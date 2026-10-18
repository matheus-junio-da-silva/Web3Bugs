// Project 13 — historical Notional Finance V2; original property is verbatim.
// Property: impliedRateSlippageDoesNotChangeWithTime; instance 36; Status: incomplete.
// Original property: certora/asset/LiquidityCurve.spec:237-261
// Included original CVL ranges: certora/asset/LiquidityCurve.spec:1-1; certora/asset/LiquidityCurve.spec:4-4; certora/asset/LiquidityCurve.spec:10-10; certora/asset/LiquidityCurve.spec:11-11; certora/asset/LiquidityCurve.spec:28-28; certora/asset/LiquidityCurve.spec:29-29; certora/asset/LiquidityCurve.spec:30-30; certora/asset/LiquidityCurve.spec:237-261
// No migration to CVL2.

methods {
    getRateScalar(uint256 timeToMaturity) returns (int256) envfree;
    getLastImpliedRate() returns (uint256) envfree;
    MATURITY() returns (uint256) envfree;
    executeTrade(uint256 timeToMaturity, int256 fCashToAccount) returns (int256,int256) envfree;
}

definition absDiff(uint256 x, uint256 y) returns uint256 = x > y ? x - y : y - x;

definition basisPoint() returns uint256 = 100000;

definition QUARTER() returns uint256 = 86400 * 90;

rule impliedRateSlippageDoesNotChangeWithTime(
    int256 fCashToAccount,
    uint256 timeDelta
) {
    env e;
    // Ensure that the block time is within the tradeable region
    require timeDelta <= QUARTER() && e.block.timestamp + timeDelta < MATURITY();
    require fCashToAccount != 0;
    uint256 timeToMaturity_first = MATURITY() - e.block.timestamp;
    uint256 timeToMaturity_second = MATURITY() - e.block.timestamp - timeDelta;
    require getRateScalar(timeToMaturity_first) > 0;
    require getRateScalar(timeToMaturity_second) > 0;

    storage initStorage = lastStorage;
    executeTrade(timeToMaturity_first, fCashToAccount);
    uint256 lastImpliedRate_first = getLastImpliedRate();

    executeTrade(timeToMaturity_second, fCashToAccount) at initStorage;
    uint256 lastImpliedRate_second = getLastImpliedRate();

    require lastImpliedRate_first < 1000000 && lastImpliedRate_second < 1000000;

    assert absDiff(lastImpliedRate_first, lastImpliedRate_second) < basisPoint(),
        "Last implied rate slippage increases with time";
}
