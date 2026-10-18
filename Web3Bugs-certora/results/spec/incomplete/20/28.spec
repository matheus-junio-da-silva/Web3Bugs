// Project 20 - Sushi BentoBox, historical CVL; no CVL2 migration.
// Source: contracts/20/spec/rebase.spec:137-151 (literal property below)
// Target-specific execution context recorded in companion documentation.
methods {
    getElastic() returns (uint128) envfree;
    getBase() returns (uint128) envfree;
    toBase(uint256 elastic, bool roundUp) returns (uint256 base) envfree;
    toElastic(uint256 base, bool roundUp) returns (uint256 elastic) envfree;
}

definition only_slightly_larger_than(uint x, uint y, uint epsilon) returns bool = y <= x && x <= y + epsilon;

rule toElasticAndToBaseAreInverse2down {
    bool roundUp = false;
    uint128 base1 = getBase();
    uint128 elastic1 = getElastic();

    require base1 != 0 && elastic1 != 0;

    uint256 amount;

    uint256 amountToBase = toBase(amount, roundUp);
    uint256 amountToBaseToElastic = toElastic(amountToBase, roundUp);

    uint256 error_margin2 = elastic1 / base1 + 1; 
    assert only_slightly_larger_than(amount, amountToBaseToElastic, error_margin2);
}
