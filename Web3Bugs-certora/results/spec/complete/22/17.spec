// Popsicle V3 Optimizer historical CVL; original source: contracts/22/spec/PopsicleV3Optimizer.spec
// Exact original source intervals: 13-15;26-85;326-346
// Original spec lines 13-15
using DummyERC20A as token0
using DummyERC20B as token1
using SymbolicUniswapV3Pool as pool

// Original spec lines 26-85
methods {
	//math functions
	floor(int24 tick, int24 tickSpacing) => NONDET
	getSqrtRatioAtTick(int24 tick) => NONDET
	getTickAtSqrtRatio(uint160 sqrtPriceX96) => NONDET
    sqrt(uint256 x) => approximateSqrt(x)
	// mulDiv(uint256 a, uint256 b, uint256 denominator) => NONDET
	mulDivRoundingUp(uint256 a, uint256 b, uint256 denominator) => NONDET
	
    
    getPositionTicks(address pool, uint256 amount0Desired, uint256 amount1Desired, int24 baseThreshold, int24 tickSpacing) => NONDET
	amountsForTicks(address pool, uint256 amount0Desired, uint256 amount1Desired, int24 _tickLower, int24 _tickUpper) => NONDET
	baseTicks(int24 currentTick, int24 baseThreshold, int24 tickSpacing) => NONDET
	amountsDirection(uint256 amount0Desired, uint256 amount1Desired, uint256 amount0, uint256 amount1) => NONDET
	checkDeviation(address pool, int24 maxTwapDeviation, uint32 twapDuration) => NONDET
	getTwap(address pool, uint32 twapDuration) => NONDET

	//interface IOptimizerStrategy 
    maxTotalSupply() => NONDET
    twapDuration() => NONDET
	maxTwapDeviation() => NONDET
	tickRangeMultiplier() => NONDET
	priceImpactPercentage() => NONDET

    balanceOf(address) returns(uint256) envfree
    totalSupply() returns(uint256) envfree

    //harness
    position_Liquidity() returns(uint128) envfree
    protocol_Liquidity() returns(uint128) envfree
    governance() returns(address) envfree
    protocolFees0() returns (uint256) envfree
    protocolFees1() returns (uint256) envfree
    totalFees0() returns (uint256) envfree
    totalFees1() returns (uint256) envfree
    token0.balanceOf(address) returns(uint256) envfree
    token1.balanceOf(address) returns(uint256) envfree
    pool.liquidity() returns (uint256) envfree
    pool.balance0() returns (uint256) envfree
    pool.balance1() returns (uint256) envfree
    pool.owed0() returns (uint128) envfree
    pool.owed1() returns (uint128) envfree
    

	// pool callback
	uniswapV3MintCallback(
        uint256 amount0,
        uint256 amount1,
        bytes data
    ) => DISPATCHER(true)

	uniswapV3SwapCallback(
        int256 amount0,
        int256 amount1,
        bytes  data
    ) => DISPATCHER(true)

}

ghost approximateSqrt(uint256) returns uint256;

// Original spec lines 326-346
rule totalSupply_vs_positionAmounts(method f){
   env e;

   uint256 totalSupplyBefore = totalSupply();
   uint256 posLiquidityBefore = position_Liquidity();

    require governance() != currentContract;
    require governance() != pool;

   require lastCompoundLiquidity(e) == 0;

   calldataarg args;
	f(e,args);

   uint256 totalSupplyAfter = totalSupply();
   uint256 posLiquidityAfter = position_Liquidity();   
   uint256 compoundAfter = lastCompoundLiquidity(e);

    assert totalSupplyAfter < totalSupplyBefore =>
            posLiquidityAfter - compoundAfter < posLiquidityBefore;
}

