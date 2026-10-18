// Popsicle V3 Optimizer historical CVL; original source: contracts/22/spec/PoolActions.spec
// Exact original source intervals: 2-9;29-45
// Original spec lines 2-9
methods {

    transfer(address,uint) => DISPATCHER(true)
    balanceOf(address) => DISPATCHER(true)
    transferFrom(address,address,uint) => DISPATCHER(true)
    // mint(uint256) => DISPATCHER(true)

}

// Original spec lines 29-45
rule checkBurnExactLiquidity(
        int24 tickLower,
        int24 tickUpper,
        uint128 liquidity
    ){
        env e;
        require to == e.msg.sender;
        uint256 amount0;
        uint256 amount1;
        amount0, amount1 = callBurnExactLiquidity(e,
            tickLower,
            tickUpper,
            liquidity,
            e.msg.sender);
        assert liquidity == 0 => amount0 == 0 && amount1 == 0;
        assert liquidity > 0 => amount0 > 0 || amount1 > 0;// && (amount0 <= liquidity || amount1 <= liquidity);
}

