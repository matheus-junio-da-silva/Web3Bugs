// Literal Solidity excerpt: contracts/22/contracts/popsicle-v3-optimizer/PopsicleV3Optimizer.sol:194-243
     function deposit(
        uint256 amount0Desired,
        uint256 amount1Desired,
        address to
    )
        external
        override
        nonReentrant
        checkDeviation
        whenNotPaused
        returns (
            uint256 shares,
            uint256 amount0,
            uint256 amount1
        )
    {
        _earnFees();
        _compoundFees(); // prevent user drains others
        (uint256 usersAmount0, uint256 usersAmount1) = pool.usersAmounts(tickLower, tickUpper);
        usersAmount0 = usersAmount0.add(_balance0().unsafeDiv(2)); // prevent draining
        usersAmount1 = usersAmount1.add(_balance1().unsafeDiv(2));
        
        // compute the liquidity amount
        uint128 liquidity = pool.liquidityForAmounts(amount0Desired, amount1Desired, tickLower, tickUpper);
        
        (amount0, amount1) = pool.mint(
            address(this),
            tickLower,
            tickUpper,
            liquidity,
            abi.encode(MintCallbackData({payer: msg.sender})));
        
        require(amount0 > 0 && amount1 > 0, "ANV");
        uint256 shares0 = 
            totalSupply() == 0 
            ? liquidity
            : FullMath.mulDiv(amount0, totalSupply(), usersAmount0);
        
        uint256 shares1 = 
            totalSupply() == 0 
            ? liquidity
            : FullMath.mulDiv(amount1, totalSupply(), usersAmount1);
        shares =  shares0 < shares1 ? shares0 : shares1;

        _mint(to, shares);
        require(IOptimizerStrategy(strategy).maxTotalSupply() >= totalSupply(), "MTS");
        emit Deposit(msg.sender, to, shares, amount0, amount1);
    }
    
    /// @inheritdoc IPopsicleV3Optimizer

// Literal Solidity excerpt: contracts/22/contracts/popsicle-v3-optimizer/PopsicleV3Optimizer.sol:284-312
    function withdraw(
        uint256 shares,
        address to
    ) 
        external
        override
        nonReentrant
        checkDeviation
        whenNotPaused
        returns (
            uint256 amount0,
            uint256 amount1
        )
    {
        require(shares > 0, "S");
        require(to != address(0), "WZA");
        _earnFees();
        _compoundFees();
        (amount0, amount1) = pool.burnLiquidityShare(tickLower, tickUpper, totalSupply(), shares,  to);
        require(amount0 > 0 || amount1 > 0, "EA");
        uint256 imbalancedAmount0 = FullMath.mulDiv(_balance0(), shares, totalSupply());
        uint256 imbalancedAmount1 = FullMath.mulDiv(_balance1(), shares, totalSupply());
        if (imbalancedAmount0 > 0) pay(token0, address(this), to, imbalancedAmount0);
        if (imbalancedAmount1 > 0) pay(token1, address(this), to, imbalancedAmount1);
        // Burn shares
        _burn(msg.sender, shares);
        
        emit Withdraw(msg.sender, to, shares, amount0, amount1);
    }

// Literal Solidity excerpt: contracts/22/contracts/popsicle-v3-optimizer/PopsicleV3Optimizer.sol:448-477
uint256 public lastCompoundLiquidity;

    function _compoundFees() internal returns (uint256 amount0, uint256 amount1){
        uint256 balance0 = _balance0();
        uint256 balance1 = _balance1();

        emit Snapshot(balance0, balance1);

        //Get Liquidity for Optimizer's balances
        uint128 liquidity = pool.liquidityForAmounts(balance0, balance1, tickLower, tickUpper);
        
        // Add liquidity to the pool
        if (liquidity > 0)
        {
            (amount0, amount1) = pool.mint(
                address(this),
                tickLower,
                tickUpper,
                liquidity,
                abi.encode(MintCallbackData({payer: address(this)})));

            lastCompoundLiquidity = liquidity; //Gadi, to differientiate between compound and deposit

            emit CompoundFees(amount0, amount1);
        }
    }

    /// @notice Returns current Optimizer's position in pool
    function position() external view returns (uint128 liquidity, uint256 feeGrowthInside0LastX128, uint256 feeGrowthInside1LastX128, uint128 tokensOwed0, uint128 tokensOwed1) {
        bytes32 positionKey = PositionKey.compute(address(this), tickLower, tickUpper);

// Literal Solidity excerpt: contracts/22/contracts/popsicle-v3-optimizer/PopsicleV3Optimizer.sol:675-697
     */
    function unpause() external onlyGovernance whenPaused {
        _paused = false;
    }

    // certora helpers
    function amountInUniswapPerShare() public  returns (uint128){
        uint128 protocolLiquidity = pool.liquidityForAmounts(protocolFees0, protocolFees1, tickLower, tickUpper);
        uint128 liquidity = pool.positionLiquidity(tickLower, tickUpper);
        uint128 usersLiquidity = liquidity - protocolLiquidity;
        uint128 amountInUniswapPerShare = usersLiquidity / (uint128) (totalSupply());
        return amountInUniswapPerShare;
    }
    function protocol_Liquidity() public returns (uint128){
        uint128 protocolLiquidity = pool.liquidityForAmounts(protocolFees0, protocolFees1, tickLower, tickUpper);
        return protocolLiquidity;
    }
    function position_Liquidity() public returns (uint128){
        uint128 liquidity = pool.positionLiquidity(tickLower, tickUpper);
        return liquidity;
    }
}
