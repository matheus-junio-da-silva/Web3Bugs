// Historical source: contracts/8/specs/rayMul_rayDiv_mulDiv_properties.spec:19-30
// Property rayMul_prop_1 (rule). Rule body and dependencies copied without modification.
// CVL2 migration and missing symbolic Solidity harness reconstruction out of scope.

// Original CVL: contracts/8/specs/rayMul_rayDiv_mulDiv_properties.spec:1-18
import "methods_base.spec"

methods {
    Underlying.totalSupply() envfree;
    havoc_all() envfree;
    _SymbolicLendingPoolL1.getLiquidityIndex() envfree;

    rayMul__(uint256 a,uint256 b) returns (uint256) envfree;
    rayDiv__(uint256 a,uint256 b) returns (uint256) envfree ;
    mulDiv__(uint256 x, uint256 y, uint256 deno, uint8 rounding) returns(uint256) envfree;

    //    mulDiv(uint256 x, uint256 y, uint256 denominator) returns uint256 => mulDiv3_g(x,y,denominator);
    
    havoc_all_dummy() => HAVOC_ALL;
}




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

// Original CVL: contracts/8/specs/rayMul_rayDiv_mulDiv_properties.spec:19-30
rule rayMul_prop_1() {
    uint256 x;
    uint256 ind;
    uint256 z;
    
    require (RAY() <= ind);
    require (ind <= 2*RAY());

    uint256 a = rayMul__(to_uint256(rayDiv__(x,ind)+z),ind);
    uint256 b = to_uint256(x+rayMul__(z,ind));
    assert a==b || a==b+1 || b==a+1;
}

