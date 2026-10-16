// Project 6 - Aave Static aToken
// Extracted active property: getClaimableRewards_stable_after_deposit
// Status: incomplete; property and available CVL dependencies are copied literally below.
// CVL1/CVL2 migration is intentionally not performed.

// Original source: StaticATokenLM.spec:1-1
import "erc20.spec"

// Original source: StaticATokenLM.spec:3-10
using AToken as _AToken 
using RewardsControllerHarness as _RewardsController 
using DummyERC20_aTokenUnderlying as _DummyERC20_aTokenUnderlying 
using DummyERC20_rewardToken as _DummyERC20_rewardToken 
using SymbolicLendingPoolL1 as _SymbolicLendingPoolL1 
using TransferStrategyHarness as _TransferStrategy
using StaticATokenLMHarness as _StaticATokenLM
using ScaledBalanceTokenHarness as _ScaledBalanceToken

// Original source: StaticATokenLM.spec:12-13
methods
{

// Original source: StaticATokenLM.spec:19-20
    getRewardTokensLength() returns (uint256) envfree 
    getRewardToken(uint256) returns (address) envfree

// Original source: StaticATokenLM.spec:29-29
    _RewardsController.getAvailableRewardsCount(address) returns (uint128) envfree

// Original source: StaticATokenLM.spec:31-31
    _RewardsController.getRewardsByAsset(address,uint128) returns (address ) envfree

// Original source: StaticATokenLM.spec:42-94
    /*******************
    *     Pool.sol     *
    ********************/

    //getReserveNormalizedIncome(address) returns (uint256) => ALWAYS(1000000000000000000000000000)

    //Called by RewardsController.sol
    //Defined in RewardsDistributor.sol
    getAssetIndex(address, address) returns (uint256, uint256) =>  DISPATCHER(true)
    
    //Called by AToken.sol
    //Defined in SupplyLogic.sol
    finalizeTransfer(address, address, address, uint256, uint256, uint256) => NONDET  

    //Called by getAssetIndex
    // Defined in ScaledBalanceTokenBase.sol
    scaledTotalSupply() returns (uint256) envfree => DISPATCHER(true) 
    

   /*****************************
    *     OZ ERC20Permit.sol     *
    ******************************/
    permit(address,address,uint256,uint256,uint8,bytes32,bytes32) => NONDET

    /*********************
    *     AToken.sol     *
    **********************/
    mint(address,address,uint256,uint256) returns (bool) => DISPATCHER(true)
    burn(address,address,uint256,uint256) returns (bool) => DISPATCHER(true)
    getIncentivesController() returns (address) => CONSTANT
    UNDERLYING_ASSET_ADDRESS() returns (address) => CONSTANT
    
    /**********************************
    *     RewardsDistributor.sol     *
    **********************************/
    getRewardsList() returns (address[]) => NONDET

    /**********************************
    *     RewardsController.sol     *
    **********************************/

    //Called by IncentivizedERC20.sol and by StaticATokenLM.sol
    handleAction(address,uint256,uint256) => DISPATCHER(true)

    //Called by RewardsController.sol
    //Defined in ScaledBalanceTokenBase.sol
    getScaledUserBalanceAndSupply(address) returns (uint256, uint256) => DISPATCHER(true)

    //Called by RewardsController._transferRewards()
    //Defined in TransferStrategyHarness as simple transfer() 
    performTransfer(address,address,uint256) returns (bool) =>  DISPATCHER(true)

 }

// Original source: StaticATokenLM.spec:514-553
rule getClaimableRewards_stable_after_deposit()
{
    env e;
    address user;
    address reward;
    
    uint256 assets;
    address recipient;
    uint16 referralCode;
    bool fromUnderlying = true;

    require user != 0;

    require getRewardTokensLength() == 1;

    require _RewardsController.getAvailableRewardsCount(_AToken)  > 0;
    require _RewardsController.getRewardsByAsset(_AToken, 0) == _DummyERC20_rewardToken;

    require currentContract != user;
    require _AToken != user;
    require _RewardsController !=  user;
    require _DummyERC20_aTokenUnderlying  != user;
    require _DummyERC20_rewardToken != user;
    require _SymbolicLendingPoolL1 != user;
    require _TransferStrategy != user;
    require _ScaledBalanceToken != user;
    require _TransferStrategy != user;

    //assume a single reward
    require reward == _DummyERC20_rewardToken;
    require getRewardTokensLength() == 1;
    require getRewardToken(0) == _DummyERC20_rewardToken;
    
    //require isRegisteredRewardToken(reward); //todo: review the assumption
 
    mathint claimableRewardsBefore = getClaimableRewards(e, user, reward);
    deposit(e, assets, recipient,referralCode,fromUnderlying);
    mathint claimableRewardsAfter = getClaimableRewards(e, user, reward);
    assert claimableRewardsAfter == claimableRewardsBefore;
}
