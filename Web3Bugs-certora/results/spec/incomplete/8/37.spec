// Source: PropertyGPT/certora_projects/aave_vault; Project 8, example 37.
// Original property body preserved verbatim; no ghost axioms normalized or repaired.
// Shared imports are inlined selectively without duplicated import statements.
// Historical CVL syntax not migrated. No Certora Prover run has been reproduced.

// Original CVL: contracts/8/specs/methods_base.spec:65 (shared constants)
definition RAY() returns uint256 = 10^27;


// Original CVL: contracts/8/specs/rayMul_rayDiv_mulDiv_properties.spec:8-9
methods {
    rayMul__(uint256 a,uint256 b) returns (uint256) envfree;
    rayDiv__(uint256 a,uint256 b) returns (uint256) envfree ;
}


// Original CVL: contracts/8/specs/rayMul_rayDiv_mulDiv_properties.spec:33-44
rule rayMul_prop_2() {
    uint256 x;
    uint256 ind;
    uint256 z;
    
    require (RAY() <= ind);
    require (ind <= 2*RAY());

    uint256 c = rayMul__(to_uint256(z-rayDiv__(x,ind)),ind);
    uint256 d = to_uint256(rayMul__(z,ind)-x);
    assert c==d || c==to_uint256(d+1) || d==to_uint256(c+1);
}

