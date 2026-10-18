// Project 20 - Sushi BentoBox, historical CVL; no CVL2 migration.
// Source: contracts/20/spec/rebase.spec:48-56 (literal property below)
// Target-specific execution context recorded in companion documentation.
methods {
    toBase(uint256 elastic, bool roundUp) returns (uint256 base) envfree;
}

rule toBaseIsMonotone {
    bool roundUp;
    uint x;
    uint y;
    require x < y;
    uint xToBase = toBase(x, roundUp);
    uint yToBase = toBase(y, roundUp);
    assert xToBase <= yToBase; 
}
