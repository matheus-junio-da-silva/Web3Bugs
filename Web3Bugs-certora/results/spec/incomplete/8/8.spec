// Source: PropertyGPT/certora_projects/aave_vault; Project 8, example 8.
// Original property body preserved verbatim; no ghost axioms normalized or repaired.
// Shared imports are inlined selectively without duplicated import statements.
// Historical CVL syntax not migrated. No Certora Prover run has been reproduced.

// Original CVL: contracts/8/specs/methods_base.spec:3 (using declarations)
using AToken as _AToken

// Original CVL: contracts/8/specs/methods_base.spec:13;14;16;18;20;21;28 (selected method declarations)
methods {
    maxDeposit(address) returns (uint256) envfree;
    maxRedeem(address) returns (uint256);
    getFee() returns (uint256) envfree
    totalSupply() returns uint256 envfree
    getLastVaultBalance() returns (uint256) envfree;
    getAccumulatedFees() returns (uint128) envfree;
    _AToken.balanceOf(address) returns (uint256) envfree;
}

// Original CVL: contracts/8/specs/methods_base.spec:68 (shared constants)
definition SCALE() returns uint256 = 1000000000000000000;

// Original CVL: contracts/8/specs/methods_base.spec:207-207
function maxUint128() returns uint128 {return 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF;}


// Original CVL: contracts/8/specs/erc4626.spec:2-72

//using DummyContract as _DummyContract

methods {
    rayMul(uint256 a,uint256 b) returns (uint256) => rayMul_g(a,b);
    rayDiv(uint256 a,uint256 b) returns (uint256) => rayDiv_g(a,b);
    havoc_all() envfree;
    
    havoc_all_dummy() => HAVOC_ALL;
    mulDiv(uint256 x, uint256 y, uint256 denominator) returns uint256 => mulDiv3_g(x,y,denominator);
    //mulDiv(uint256 x, uint256 y, uint256 denominator, uint8 rounding) returns uint256 => mulDiv4_g(x,y,denominator,rounding) ;
}

/*
function mulDiv4_g(uint256 x, uint256 y, uint256 denominator, uint8 rounding) returns uint256 {
    uint256 result = mulDiv3_g(x, y, denominator);

    require (denominator != 0);
    mathint mulmod = (x*y) % denominator;
    if (rounding == 1 && mulmod > 0) {
        result = result + 1;
    }
    return result;
    }*/

ghost mulDiv3_g(uint256 , uint256 , uint256) returns uint256 {
    axiom 1==1;
}
ghost rayMul_g(uint256 , uint256) returns uint256 {
    axiom 1==1;
}
ghost rayDiv_g(uint256 , uint256) returns uint256 {
    axiom 1==1;
}


// ****************************************************************
// By EIP4626, the following functions must not revert
// ****************************************************************
function f_must_NOT_revert(method f) returns bool {
    return 
        f.selector == asset().selector ||
        f.selector == totalAssets().selector ||
        f.selector == maxDeposit(address).selector ||
        f.selector == maxMint(address).selector ||
        f.selector == maxWithdraw(address).selector ||
        f.selector == maxRedeem(address).selector
    ;
}


// ****************************************************************
// By EIP4626, the following functions:
// MUST NOT revert unless due to integer overflow caused by an unreasonably large input.
// ****************************************************************
function f_must_NOT_revert_unless_large_input(method f) returns bool {
    return
        f.selector == convertToShares(uint256).selector ||
        f.selector == convertToAssets(uint256).selector
        ;
}


// ****************************************************************
// By EIP4626: the functions: asset, totalAssets, maxDeposit, maxMint, maxWithdraw, maxRedeem
// must not revert.
//
// STATUS: fail
// - asset() indeed does not revert.
// - All the other function may revert due to arithmetical calculations.
// ****************************************************************


// Original CVL: contracts/8/specs/erc4626.spec:211-233
rule previewMint_amount_check() {
    env e1;
    env e2;
    uint256 shares;
    address receiver;
    uint256 previewAssets;
    uint256 assets;

    require e1.block.timestamp <= e2.block.timestamp;
    require e2.block.timestamp <= 0xffffff;

    require _AToken.balanceOf(currentContract) <= maxUint128();
    require getAccumulatedFees() <= maxUint128();
    require getLastVaultBalance() <= maxUint128();
    require totalSupply() <= maxUint128();

    require(getFee() <= SCALE());  // SCALE is 10^18
        
    previewAssets = previewMint(e1,shares);
    require (shares <= convertToShares(e2,maxDeposit(receiver)) => convertToAssets(e2,shares) <= maxDeposit(receiver));
    assets = mint(e2, shares, receiver);
    assert previewAssets == assets || previewAssets == assets+1 || previewAssets+1 == assets, "preview should be equal to actual - mint";
}

