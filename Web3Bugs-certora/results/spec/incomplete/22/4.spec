// Popsicle V3 Optimizer historical CVL; original source: contracts/22/spec/PoolActions.spec
// Exact original source intervals: 2-9;10-25
// Original spec lines 2-9
methods {

    transfer(address,uint) => DISPATCHER(true)
    balanceOf(address) => DISPATCHER(true)
    transferFrom(address,address,uint) => DISPATCHER(true)
    // mint(uint256) => DISPATCHER(true)

}

// Original spec lines 10-25
rule checkBurnLiquidityShare(
        int24 tickLower,
        int24 tickUpper,
        uint256 share,
        address to){
    env e;
    require (share > 0 && share <= totalSupply());
    uint256 totalSupplyBefore = totalSupply();
    uint256 amount0;
    uint256 amount1;
    amount0, amount1 = callBurnLiquidityShare(e, tickLower, tickUpper, share, 
                       e.msg.sender);
    assert(totalSupply() == totalSupplyBefore);
    assert(!lastReverted);
    
}

