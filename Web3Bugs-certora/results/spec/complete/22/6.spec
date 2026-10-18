// Popsicle V3 Optimizer historical CVL; original source: contracts/22/spec/PoolActions.spec
// Exact original source intervals: 2-9;47-52
// Original spec lines 2-9
methods {

    transfer(address,uint) => DISPATCHER(true)
    balanceOf(address) => DISPATCHER(true)
    transferFrom(address,address,uint) => DISPATCHER(true)
    // mint(uint256) => DISPATCHER(true)

}

// Original spec lines 47-52
rule checkBurnAllLiquidity(int24 tickLower,
                        int24 tickUpper){
    callBurnAllLiquidity(tickLower, tickUpper);
    // uint128 liquidity = pool.positionLiquidity(tickLower, tickUpper);
    // assert(liquidity ==0);
}
