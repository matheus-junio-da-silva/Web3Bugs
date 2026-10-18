// Popsicle V3 Optimizer historical CVL; original source: contracts/22/spec/FullMathWrapper.spec
// Exact original source intervals: 22-38
// Original spec lines 22-38
rule integrityOfMulDiv(uint256 a,
             uint256 b,
             uint256 denominator){
    /* require(denominator > 0 && a*(b/denominator) >= 0 && b*(a/denominator) >= 0 &&
            a*(b/denominator) <= 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff &&
            b*(a/denominator) <= 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff); */
    env e;

    uint256 mul = a * b;
    /* uint256 remainder = mul % denominator; 
    uint256 truncated = (a * b) - remainder; */
    uint256 result = callMulDiv(e , a,
             b,
             denominator);
    
    assert (result == a*b/denominator || a==0 || b==0);
}

