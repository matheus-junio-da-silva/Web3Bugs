// Literal Solidity excerpt: contracts/22/spec/harness/SymbolicUniswapV3Pool.sol:41-80
contract SymbolicUniswapV3Pool is IUniswapV3Pool {
    uint256 public liquidity;
    uint256 public ratio;
    address public immutable override token0;
    address public immutable override token1;
    uint128 public owed0;
    uint128 public owed1;
    using LowGasSafeMath for uint256;
    using LowGasSafeMath for uint128;
    using LowGasSafeMath for int256;
    using PoolVariables for IUniswapV3Pool;

    constructor(address _token0, address _token1) {
        token0 = _token0;
        token1 = _token1;
        ratio = 4;
    }

    function balance0() public view returns (uint256) {
        return IERC20(token0).balanceOf(address(this));
    }

    /// @dev Get the pool's balance of token1
    /// @dev This function is gas optimized to avoid a redundant extcodesize check in addition to the returndatasize
    /// check
    function balance1() public view returns (uint256) {
        return IERC20(token1).balanceOf(address(this));
    }


     function liquidityForAmounts(
        IUniswapV3Pool pool,
        uint256 amount0,
        uint256 amount1,
        int24 _tickLower,
        int24 _tickUpper
    ) public view returns (uint128) {
        return pool.liquidityForAmounts(amount0, amount1, _tickLower, _tickUpper);
    }


// Literal Solidity excerpt: contracts/22/spec/harness/SymbolicUniswapV3Pool.sol:92-185
    function mint(
        address recipient,
        int24 tickLower,
        int24 tickUpper,
        uint128 amount,
        bytes calldata data
    ) external override returns (uint256 amount0, uint256 amount1) {
        require(ratio == 1 || ratio == 2 || ratio == 4);
        liquidity = liquidity.add(amount);
        amount0 = amount;
        amount1 = uint256(amount).mul(ratio);
        uint256 token0Balance = balance0();
        uint256 token1Balance = balance1();
        IUniswapV3MintCallback(msg.sender).uniswapV3MintCallback(
            amount0,
            amount1,
            data
        );
        //maybe add require that now the balance increased as expected
        require(balance0() >= token0Balance.add(amount0));
        require(balance1() >= token1Balance.add(amount1));
    }

    /// @notice Collects tokens owed to a position
    /// @dev Does not recompute fees earned, which must be done either via mint or burn of any amount of liquidity.
    /// Collect must be called by the position owner. To withdraw only token0 or only token1, amount0Requested or
    /// amount1Requested may be set to zero. To withdraw all tokens owed, caller may pass any value greater than the
    /// actual tokens owed, e.g. type(uint128).max. Tokens owed may be from accumulated swap fees or burned liquidity.
    /// @param recipient The address which should receive the fees collected
    /// @param tickLower The lower tick of the position for which to collect fees
    /// @param tickUpper The upper tick of the position for which to collect fees
    /// @param amount0Requested How much token0 should be withdrawn from the fees owed
    /// @param amount1Requested How much token1 should be withdrawn from the fees owed
    /// @return amount0 The amount of fees collected in token0
    /// @return amount1 The amount of fees collected in token1
    function collect(
        address recipient,
        int24 tickLower,
        int24 tickUpper,
        uint128 amount0Requested,
        uint128 amount1Requested
    ) external override returns (uint128 amount0, uint128 amount1) {
        if (amount0Requested >= owed0) {
            amount0 = owed0;
            owed0 = 0;
        } else {
            owed0 = owed0.sub128(amount0Requested);
            amount0 = amount0Requested;
        }
        IERC20(token0).transfer(recipient, amount0);
        if (amount1Requested >= owed1) {
            amount1 = owed1;
            owed1 = 0;
        } else {
            owed1 = owed1.sub128(amount1Requested);
            amount1 = amount1Requested;
        }
        IERC20(token1).transfer(recipient, amount1);
    }

    /// @notice Burn liquidity from the sender and account tokens owed for the liquidity to the position
    /// @dev Can be used to trigger a recalculation of fees owed to a position by calling with an amount of 0
    /// @dev Fees must be collected separately via a call to #collect
    /// @param tickLower The lower tick of the position for which to burn liquidity
    /// @param tickUpper The upper tick of the position for which to burn liquidity
    /// @param amount How much liquidity to burn
    /// @return amount0 The amount of token0 sent to the recipient
    /// @return amount1 The amount of token1 sent to the recipient
    function burn(
        int24 tickLower,
        int24 tickUpper,
        uint128 amount
    ) external override returns (uint256 amount0, uint256 amount1) {
        require(ratio == 1 || ratio == 2 || ratio == 4);
        require(liquidity >= amount);
        amount0 = amount;
        amount1 = amount.mul(ratio);
        liquidity = liquidity.sub(amount);

        require(amount0 < 2**128);
        require(amount1 < 2**128);

        owed0 = owed0.add128(uint128(amount0));
        owed1 = owed1.add128(uint128(amount1));
    }

    /// @notice Swap token0 for token1, or token1 for token0, rate does not change so limit amout to 100, and pool creator must tarnsfer to it huge amount of token0 and token1
    /// @dev The caller of this method receives a callback in the form of IUniswapV3SwapCallback#uniswapV3SwapCallback
    /// @param recipient The address to receive the output of the swap
    /// @param zeroForOne The direction of the swap, true for token0 to token1, false for token1 to token0
    /// @param amountSpecified The amount of the swap, which implicitly configures the swap as exact input (positive), or exact output (negative)
    /// @param sqrtPriceLimitX96 The Q64.96 sqrt price limit. If zero for one, the price cannot be less than this
    /// value after the swap. If one for zero, the price cannot be greater than this value after the swap
    /// @param data Any data to be passed through to the callback

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
