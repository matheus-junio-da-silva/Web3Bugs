// Popsicle V3 Optimizer historical CVL; original source: contracts/22/spec/FullMathWrapper.spec
// Exact original source intervals: 2-19
// Original spec lines 2-19
rule integrityOfMulDivNoOverflow(uint256 a,
             uint256 b,
             uint256 denominator){
    require(denominator > 0x0 && a*b <= max_uint256);
    env e;

    uint256 mul = a * b;
    uint256 remainder = mul % denominator;
    uint256 truncated = (a * b) - remainder;
    uint256 result = callMulDiv(e , a,
             b,
             denominator);
    /*
    assert ((denominator > 0 &&
    (denominator < 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff)) => (result == truncated/denominator));
    */
    assert (result == a*b/denominator);
}

