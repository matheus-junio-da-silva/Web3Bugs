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
