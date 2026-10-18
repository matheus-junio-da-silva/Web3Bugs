// Project 20 - Sushi BentoBox, historical CVL; no CVL2 migration.
// Source: contracts/20/spec/rebase.spec:61-69 (literal property below)
// Target-specific execution context recorded in companion documentation.
methods {
    toElastic(uint256 base, bool roundUp) returns (uint256 elastic) envfree;
}

rule toElasticIsMonotone {
    bool roundUp;
    uint x;
    uint y;
    require x < y;
    uint xToElastic = toElastic(x, roundUp);
    uint yToElastic = toElastic(y, roundUp);
    assert xToElastic <= yToElastic; 
}
