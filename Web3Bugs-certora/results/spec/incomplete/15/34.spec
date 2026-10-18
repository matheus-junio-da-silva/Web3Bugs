// HELIX Project 15 historical CVL extraction
// Source contracts/15/ghoAToken.spec property lines 97-132
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
invariant userBalanceAlwaysZero(address user)
	scaledBalanceOf(user) == 0



// /**
// * @title first handleRepayment(amount) after transferUnderlyingTo(amount) succeeds.
// * @dev assumption of sufficient balanceOf(msg.sender) is justified because BorrowLogic.executeRepay()
// * @dev executes: IERC20(params.asset).safeTransferFrom(msg.sender, reserveCache.aTokenAddress, paybackAmount);
// * @dev before invocation of handleRepayment()
// * OBSOLETE - GhoToken has other rules to validate the behavior of the facilitator level maintenance
// */
// rule handleRepayment_after_transferUnderlyingTo()
// {
// 	env e;
// 	calldataarg arg;
// 	uint256 amount;
// 	address target;
// 	address user;
//     address onBehalfOf;

// 	transferUnderlyingTo(e, target, amount);

// 	require _ghoTokenHarness.balanceOf(e.msg.sender) >= amount; //underlying asset
// 	require e.msg.sender == currentContract;

// 	handleRepayment@withrevert(e, user, onBehalfOf, amount);
// 	assert !lastReverted, "handleRepayment failed";

// }


/**
* @title BucketLevel decreases after transferUnderlyingTo() followed by handleRepayment()
* @dev repayment funds are, partially or fully, transferred to the treasury
*/
