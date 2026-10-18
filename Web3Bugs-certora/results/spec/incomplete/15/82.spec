// HELIX Project 15 historical CVL extraction
// Source contracts/15/ghoVariableDebtToken.spec property lines 573-590
// Historic syntax unchanged; dependency-incomplete, no CVL2 migration

// Original CVL non-property helpers from contracts/15/VariableDebtToken.spec
methods {
	// summarization for elimination the raymul operation in balance of and totalSupply.
	//getReserveNormalizedVariableDebt(address asset) returns (uint256) => indexAtTimestamp(e.block.timestamp)
	//setAdditionalData(address user, uint128 data) envfree
    handleAction(address, uint256, uint256) => NONDET
	scaledBalanceOfToBalanceOf(uint256) returns (uint256) envfree
    //balanceOf(address) returns (uint256) envfree
}

definition ray() returns uint = 1000000000000000000000000000; // 10^27
definition wad() returns uint = 1000000000000000000; // 10^18
definition bound(uint256 index) returns uint = ((index / ray()) + 1 ) / 2;
// summerization for scaledBlanaceOf -> regularBalanceOf + 0.5 (canceling the rayMul)
// ghost gRNVB() returns uint256 {
// 	axiom gRNVB() == 7 * ray();
// }
/*
Due to rayDiv and RayMul Rounding (+ 0.5) - blance could increase by (gRNI() / Ray() + 1) / 2.
*/
definition bounded_error_eq(uint x, uint y, uint scale, uint256 index) returns bool = x <= y + (bound(index) * scale) && x + (bound(index) * scale) >= y;



definition disAllowedFunctions(method f) returns bool = 
            f.selector == transfer(address, uint256).selector ||
            f.selector == allowance(address, address).selector ||
            f.selector == approve(address, uint256).selector ||
            f.selector == transferFrom(address, address, uint256).selector ||
            f.selector == increaseAllowance(address, uint256).selector ||
            f.selector == decreaseAllowance(address, uint256).selector;


ghost sumAllBalance() returns uint256 {
    init_state axiom sumAllBalance() == 0;
}

hook Sstore _userState[KEY address a].balance uint128 balance (uint128 old_balance) STORAGE {
  havoc sumAllBalance assuming sumAllBalance@new() == sumAllBalance@old() + balance - old_balance;
}

// Original CVL non-property helpers from contracts/15/summarizations.spec
// Definition of RAY unit
function first_term(uint256 x, uint256 y) returns uint256 { return x; }

ghost mapping(uint256 => mapping(uint256 => uint256)) rayMulSummariztionValues;
function rayMulSummariztion(uint256 x, uint256 y) returns uint256
{
	if (x == 0) || (y == 0)
	{
		return 0;
	}
	if (x == ray())
	{
		return y;
	}
	if (y == ray())
	{
		return x;
	}
	
	if (y > x)
	{
		if (y > ray())
		{
			require rayMulSummariztionValues[y][x] >= x;
		}
		if (x > ray())
		{
			require rayMulSummariztionValues[y][x] >= y;
		}
		return rayMulSummariztionValues[y][x];
	}
	else{
		if (x > ray())
		{
			require rayMulSummariztionValues[x][y] >= y;
		}
		if (y > ray())
		{
			require rayMulSummariztionValues[x][y] >= x;
		}
		return rayMulSummariztionValues[x][y];
	}
}

// Original CVL non-property helpers from contracts/15/ghoVariableDebtToken.spec
//import "erc20.spec"


using GhoDiscountRateStrategy as discStrategy

methods{
	/********************
	*	WadRayMath.sol	*
	*********************/
	rayMul(uint256 x, uint256 y) returns (uint256) envfree
	rayDiv(uint256 x, uint256 y) returns uint256 envfree

  	/***********************************
    *    PoolAddressesProvider.sol     *
    ************************************/
	getACLManager() returns(address) => CONSTANT

	/************************
    *    ACLManager.sol     *
    *************************/
	isPoolAdmin(address) returns(bool) => CONSTANT

	/******************************************************************
	*	DummyERC20WithTimedBalanceOf.sol (linked to _discountToken)   *
	*******************************************************************/
	// Internal function in DummyERC20WithTimedBalanceOf which exposes the block's timestamp and called by DummyERC20WithTimedBalanceOf::balanceOf
	_balanceOfWithBlockTimestamp(address user, uint256 ts) returns (uint256) envfree => balanceOfDiscountTokenAtTimestamp(user, ts)

  	/************************************
    *   DummyPool.sol (linked to POOL)  *
    *************************************/
	// Internal function in DummyPool which exposes the block's timestamp and called by Pool::getReserveNormalizedVariableDebt
	_getReserveNormalizedVariableDebtWithBlockTimestamp(address asset, uint256 timestamp) returns (uint256) => indexAtTimestamp(timestamp)

	/************************************
	*	GhoVariableDebtTokenHarness.sol	*
	*************************************/
	discStrategy.calculateDiscountRate(uint256, uint256) returns (uint256) envfree

	/************************************
	*	GhoVariableDebtTokenHarness.sol	*
	*************************************/
	getUserCurrentIndex(address) returns (uint256) envfree
	getUserDiscountRate(address) returns (uint256) envfree
	getUserAccumulatedDebtInterest(address) envfree
	getBalanceOfDiscountToken(address) returns (uint256)

	/********************************
	*	GhoVariableDebtToken.sol	*
	*********************************/
	totalSupply() returns(uint256) envfree
	balanceOf(address) returns (uint256)
	mint(address, address, uint256, uint256) returns (bool, uint256)
	burn(address ,uint256 ,uint256) returns (uint256)
	scaledBalanceOf(address) returns (uint256) envfree
	getBalanceFromInterest(address) returns (uint256) envfree
	rebalanceUserDiscountPercent(address)
	updateDiscountDistribution(address ,address ,uint256 ,uint256 ,uint256)
}

/**
* CVL implementation of rayMul
**/
function rayMulCVL(uint256 a, uint256 b) returns uint256 {
	return to_uint256((a * b + (ray() / 2)) / ray());
}
function rayDivCVL(uint256 a, uint256 b) returns uint256 {
	return to_uint256((a * ray() + (b / 2)) / b);
}

function getReserveNormalizedVariableDebt_1ray() returns uint256 {
	return ray();
}

function getReserveNormalizedVariableDebt_1or2ray() returns uint256 {
	uint256 index; havoc index;
	require (index==ray() || index==2*ray());
	return index;
}
function getReserveNormalizedVariableDebt_7ray() returns uint256 {
	uint256 index; havoc index;
	require (index==7*ray());
	return index;
}

//todo: check balanceof after mint (stable index), burn after balanceof

definition MAX_DISCOUNT() returns uint256 = 10000; // equals to 100% discount, in points

ghost mapping(uint256 => mapping (uint256 => uint256)) discount_ghost;
ghost mapping(uint256 => uint256) index_ghost;

/**
* Query index_ghost for the index value at the input timestamp
**/
function indexAtTimestamp(uint256 timestamp) returns uint256 {
	return index_ghost[timestamp];
}

/**
* Query discount_ghost for the [user]'s balance of discount token at [timestamp]
**/
function balanceOfDiscountTokenAtTimestamp(address user, uint256 timestamp) returns uint256 {
	return discount_ghost[user][timestamp];
}

/**
* Returns an env instance with [ts] as the block timestamp
**/
function envAtTimestamp(uint256 ts) returns env {
	env e;
	require(e.block.timestamp == ts);
	return e;
}

/**
* @title at any point in time, the user's discount rate isn't larger than 100%
**/

// Exact literal original property follows
rule integrityOfUpdateDiscountDistribution_updateIndex() {
	address sender;
	address recipient;
	uint256 senderDiscountTokenBalance;
    uint256 recipientDiscountTokenBalance;
	env e;
	uint256 amount;
	uint256 index = indexAtTimestamp(e.block.timestamp);
	updateDiscountDistribution(e, sender, recipient, senderDiscountTokenBalance, recipientDiscountTokenBalance, amount);
	assert(scaledBalanceOf(sender) > 0 => getUserCurrentIndex(sender) == index);
	assert(scaledBalanceOf(recipient) > 0 => getUserCurrentIndex(recipient) == index);
}


/**
* @title proves that updateDiscountDistribution can't effect other user's scaled balance
**/
// pass
