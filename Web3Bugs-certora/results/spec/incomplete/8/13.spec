// Historical source: contracts/8/specs/erc4626.spec:394-410
// Property previewRedeem_has_NO_threshold (rule). Rule body and dependencies copied without modification.
// CVL2 migration and missing symbolic Solidity harness reconstruction out of scope.

// Original CVL: contracts/8/specs/erc4626.spec:1-72
import "methods_base.spec"

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

// Original CVL: contracts/8/specs/methods_base.spec:1-7
import "erc20.spec"

using AToken as _AToken
using DummyERC20_aTokenUnderlying as Underlying
using SymbolicLendingPoolL1 as _SymbolicLendingPoolL1
using ATokenVaultHarness as _ATokenVaultHarness


// Original CVL: contracts/8/specs/methods_base.spec:8-63
methods{
    deposit(uint256, address) returns (uint256);
    //depositATokensWithSig(uint256, address, address, (uint8,bytes32,bytes32,uint256)) returns (uint256);
    depositATokensWithSig(uint256, address, address, _ATokenVaultHarness.EIP712Signature) returns (uint256);

    maxDeposit(address) returns (uint256) envfree;
    maxRedeem(address) returns (uint256);

    getFee() returns (uint256) envfree
    owner() returns (address) envfree
    totalSupply() returns uint256 envfree
    balanceOf(address) returns (uint256) envfree
    getLastVaultBalance() returns (uint256) envfree;
    getAccumulatedFees() returns (uint128) envfree;
    maxAssetsWithdrawableFromAave() returns (uint256) envfree;
    
    mulDivWrapper(uint256, uint256, uint256, uint8) envfree;
    previewRedeem(uint256) returns (uint256); 

    _AToken.totalSupply() returns uint256 envfree;
    _AToken.balanceOf(address) returns (uint256) envfree;
    _AToken.scaledTotalSupply() returns (uint256) envfree;
    _AToken.scaledBalanceOf(address) returns (uint256) envfree;
    _AToken.transferFrom(address,address,uint256) returns (bool);

    Underlying.balanceOf(address) returns (uint256) envfree;

    // //*********************  AToken.sol ********************************
    // // The following was copied from StaticATokenLM spec file
    // //*****************************************************************
    //    mint(address,address,uint256,uint256) returns (bool) => DISPATCHER(true)
    //burn(address,address,uint256,uint256) returns (bool) => DISPATCHER(true)
    getIncentivesController() returns (address) => CONSTANT;
    UNDERLYING_ASSET_ADDRESS() returns (address) => CONSTANT;


    // called by AToken.sol::224. A method of IPool.
    finalizeTransfer(address, address, address, uint256, uint256, uint256) => NONDET

    // called from: IncentivizedERC20.sol::207. A method of incentivesControllerLocal.
    handleAction(address,uint256,uint256) => NONDET

    // getPool() returns address => ALWAYS(100);
    getPool() returns address => NONDET;
    
    // // nissan Remark: not sure about the following 3 summarizations:

    // A method of Ipool
    // can this contract change the pool
    getReserveData(address) => CONSTANT;
    
    claimAllRewards(address[],address) => NONDET;

    // called in MetaTxHelpers.sol::27.
    isValidSignature(bytes32, bytes) => NONDET;
}

// Original CVL: contracts/8/specs/methods_base.spec:65-68
definition RAY() returns uint256 = 10^27;
definition RAY_HALF() returns uint256 = 5*10^26;
// In file Constants.sol we have "uint256 constant SCALE = 1e18;"
definition SCALE() returns uint256 = 1000000000000000000;

// Original CVL: contracts/8/specs/erc20.spec:1-12
// erc20 methods
methods {
    name()                                => DISPATCHER(true)
    symbol()                              => DISPATCHER(true)
    decimals()                            => DISPATCHER(true)
    totalSupply()                         => DISPATCHER(true)
    balanceOf(address)                    => DISPATCHER(true)
    allowance(address,address)            => DISPATCHER(true)
    approve(address,uint256)              => DISPATCHER(true)
    transfer(address,uint256)             => DISPATCHER(true)
    transferFrom(address,address,uint256) => DISPATCHER(true)
}

// Original CVL: contracts/8/specs/erc4626.spec:394-410
rule previewRedeem_has_NO_threshold(env e1, env e2) {
    require e1.block.timestamp <= e2.block.timestamp;
    require e2.block.timestamp <= 0xffffff;
    
    uint256 shares;

    uint256 total_supply_1 = totalSupply();
    uint256 total_assets_1 = totalAssets(e1);   
    uint256 preview_assets_1 = previewRedeem(e1, shares);

    havoc_all();
    require (total_supply_1 == totalSupply());
    require (total_assets_1 == totalAssets(e2));
    uint256 preview_assets_2 = previewRedeem(e2, shares);

    assert (preview_assets_1 == preview_assets_2);
}

