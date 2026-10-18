// Project 20 - Sushi BentoBox, historical CVL; no CVL2 migration.
// Source: contracts/20/spec/rebase.spec:174-191 (literal property below)
// Target-specific execution context recorded in companion documentation.
methods {
    getElastic() returns (uint128) envfree;
    getBase() returns (uint128) envfree;
    toBase(uint256 elastic, bool roundUp) returns (uint256 base) envfree;
    toElastic(uint256 base, bool roundUp) returns (uint256 elastic) envfree;
}

rule toElasticAndToBaseAreInverse0ElasticEdgeCase {
    bool roundUp;
    uint128 base1 = getBase();
    uint128 elastic1 = getElastic();

    require elastic1 == 0;

    uint256 amount;

    uint256 amountToElastic = toElastic(amount, roundUp);
    uint256 amountToElasticToBase = toBase(amountToElastic, roundUp);

    uint256 amountToBase = toBase(amount, roundUp);
    uint256 amountToBaseToElastic = toElastic(amountToBase, roundUp);

    assert amountToElasticToBase == amount  || amountToElasticToBase == 0;
    assert amountToBaseToElastic == amount || amountToBaseToElastic == 0;
}
