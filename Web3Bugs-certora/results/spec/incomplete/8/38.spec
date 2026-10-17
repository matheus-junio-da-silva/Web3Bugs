// Source: PropertyGPT/certora_projects/aave_vault; Project 8, example 38.
// Original property body preserved verbatim; no ghost axioms normalized or repaired.
// Shared imports are inlined selectively without duplicated import statements.
// Historical CVL syntax not migrated. No Certora Prover run has been reproduced.

// Original CVL: contracts/8/specs/methods_base.spec:207-207
function maxUint128() returns uint128 {return 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF;}


// Original CVL: contracts/8/specs/rayMul_rayDiv_mulDiv_properties.spec:9
methods {
    mulDiv__(uint256 x, uint256 y, uint256 deno, uint8 rounding) returns(uint256) envfree;
}


// Original CVL: contracts/8/specs/rayMul_rayDiv_mulDiv_properties.spec:46-61
rule mulDiv_properties() {
    uint256 assets;
    uint8 rnd;

    uint256 totA;
    uint256 totS;

    require (assets <= maxUint128());
    require (totA <= maxUint128());
    require (totS <= maxUint128());

    uint256 calc = mulDiv__(assets,totS,totA,rnd);

    //    assert totA-assets == 0  =>  totS-mulDiv__(assets,totS,totA,rnd) == 0;
    assert totA==assets  =>  totS == calc;
}

