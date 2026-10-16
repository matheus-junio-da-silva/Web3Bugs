// Project 6 - Aave Static aToken
// Extracted active property: totalAssets_stable_after_collectAndUpdateRewards
// Status: incomplete; property and available CVL dependencies are copied literally below.
// CVL1/CVL2 migration is intentionally not performed.

// Original source: StaticATokenLM.spec:1-1
import "erc20.spec"

// Original source: StaticATokenLM.spec:3-4
using AToken as _AToken 
using RewardsControllerHarness as _RewardsController 

// Original source: StaticATokenLM.spec:12-13
methods
{

// Original source: StaticATokenLM.spec:31-31
    _RewardsController.getRewardsByAsset(address,uint128) returns (address ) envfree

// Original source: StaticATokenLM.spec:35-35
    _RewardsController.getUserAccruedReward(address, address, address) returns (uint256) envfree

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

// Original source: StaticATokenLM.spec:297-307
rule totalAssets_stable_after_collectAndUpdateRewards()
{
    env e;
    require _RewardsController.getRewardsByAsset(_AToken, 0) != _AToken;
    require _RewardsController.getUserAccruedReward(currentContract, _AToken, _AToken) ==0;
    address reward;
    mathint totalAssetBefore = totalAssets(e);
    collectAndUpdateRewards(e, reward); 
    mathint totalAssetAfter = totalAssets(e);
    assert totalAssetAfter == totalAssetBefore;
}
