// Literal Solidity excerpt: contracts/22/spec/harness/SymbolicUniswapV3Pool.sol:41-70
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



// Literal Solidity excerpt: contracts/22/spec/harness/SymbolicUniswapV3Pool.sol:127-185
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
