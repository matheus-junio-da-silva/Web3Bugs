// Extracted from: contracts/3/specs/rescueLendMigrator.spec
// Property: LendIsBackedByAaveIncInitialize
// Dependency status: incomplete
// Original source ranges included: 1-3;5-12;41-61
// CVL2 migration is intentionally out of scope for this catalog stage.

using DummyERC20Impl as LEND1
using DummyERC20Impl2 as AAVE1
using AaveTokenV2 as AAVE_ORIG
methods{
    LEND1.balanceOf(address) returns (uint256) envfree
    AAVE1.balanceOf(address) returns (uint256) envfree
    LEND1.totalSupply() returns (uint256) envfree
    LEND_AAVE_RATIO() returns (uint256) envfree
    transfer(address, uint256) returns (bool) => DISPATCHER(true)
    onTransfer(address, address, uint256) => NONDET
}
// Shows that the property is preserved for also for initialized after AAVE.initialized is called with the same arg
rule LendIsBackedByAaveIncInitialize(env e, method f){
    require e.msg.sender != LEND1;
    require e.msg.sender != AAVE1;
    require ( (LEND1.totalSupply() - LEND1.balanceOf(LEND1)) ) / LEND_AAVE_RATIO() <= AAVE1.balanceOf(currentContract);
    
    if (f.selector == initialize(address, uint256, uint256, uint256).selector){
        address aaveMerkleDistributor; uint256 lendToMigratorAmount; uint256 lendToLendAmount; uint256 lendToAaveAmount;
        initialize(e, aaveMerkleDistributor, lendToMigratorAmount, lendToLendAmount, lendToAaveAmount);
        address lendToken = LEND1;
        address[] tokens; uint256[] amounts;
        env e2;
        AAVE_ORIG.initialize(e, tokens, amounts, aaveMerkleDistributor, lendToken, lendToAaveAmount);   
    }
    else {
        calldataarg args;
        f(e, args);
    }

    assert ( (LEND1.totalSupply() - LEND1.balanceOf(LEND1)) ) / LEND_AAVE_RATIO() <= AAVE1.balanceOf(currentContract);
}