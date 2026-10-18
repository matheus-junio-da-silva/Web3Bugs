// Popsicle V3 Optimizer historical CVL; original source: contracts/22/spec/FullMathWrapper.spec
// Exact original source intervals: 60-72
// Original spec lines 60-72
rule checkMulDivRoundingUp(uint256 a,
             uint256 b,
             uint256 denominator){
    require(denominator > 0x0 && 
             a*(b/denominator) <= 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff &&
             b*(a/denominator) <= 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff);
    env e;
    uint256 result = callMulDivRoundingUp(e , a,
             b,
             denominator);
     assert ((a *b % denominator == 0) && result == (a*b)/denominator ||
              (a *b % denominator> 0) && result == (a*b)/denominator + 1);
}

