// HELIX Project 15 historical CVL extraction
// Source contracts/15/ghoAToken.spec property lines 133-148
// Historic syntax unchanged; dependency-incomplete, no CVL2 migration

// Original CVL non-property helpers from contracts/15/erc20.spec
// erc20 methods
methods {
    name()                                returns (string)  => DISPATCHER(true)
    symbol()                              returns (string)  => DISPATCHER(true)
    decimals()                            returns (string)  => DISPATCHER(true)
    totalSupply()                         returns (uint256) => DISPATCHER(true)
    balanceOf(address)                    returns (uint256) => DISPATCHER(true)
    allowance(address,address)            returns (uint)    => DISPATCHER(true)
    approve(address,uint256)              returns (bool)    => DISPATCHER(true)
    transfer(address,uint256)             returns (bool)    => DISPATCHER(true)
    transferFrom(address,address,uint256) returns (bool)    => DISPATCHER(true)
}

// Original CVL non-property helpers from contracts/15/ghoAToken.spec

using GhoTokenHarness as _ghoTokenHarness

methods{

	totalSupply() returns (uint256) envfree
	RESERVE_TREASURY_ADDRESS() returns (address) envfree
	UNDERLYING_ASSET_ADDRESS() returns (address) envfree
	transferUnderlyingTo(address,uint256)
	handleRepayment(address,address,uint256) 
	distributeFeesToTreasury() envfree 
	rescueTokens(address,address,uint256) 
	setVariableDebtToken(address) 
	getVariableDebtToken() returns (address) envfree
	updateGhoTreasury(address) 
	getGhoTreasury() returns (address) envfree
	_ghoTokenHarness.getFacilitatorBucketCapacity(address) returns (uint256) envfree
	_ghoTokenHarness.getFacilitatorBucketLevel(address) returns (uint256) envfree
	_ghoTokenHarness.balanceOf(address) returns (uint256) envfree
	scaledBalanceOf(address) returns (uint256) envfree

  	/*******************
    *     Pool.sol     *
    ********************/
    getReserveNormalizedIncome(address) returns (uint256) => CONSTANT


  	/***********************************
    *    PoolAddressesProvider.sol     *
    ************************************/
	getACLManager() returns(address) => CONSTANT

	/************************
    *    ACLManager.sol     *
    *************************/
	isPoolAdmin(address) returns(bool) => CONSTANT


}

/**
* @title Proves that ghoAToken::mint always reverts
**/

// Exact literal original property follows
rule level_does_not_decrease_after_transferUnderlyingTo_followed_by_handleRepayment()
{
	env e;
	calldataarg arg;
	uint256 amount;
	address target;
	address user;
    address onBehalfOf;

	uint256 levelBefore = _ghoTokenHarness.getFacilitatorBucketLevel(currentContract);
	transferUnderlyingTo(e, target, amount);
	handleRepayment(e, user, onBehalfOf, amount);
	uint256 levelAfter = _ghoTokenHarness.getFacilitatorBucketLevel(currentContract);
	assert levelBefore <= levelAfter;

}
