// Literal Solidity excerpt: contracts/22/contracts/popsicle-v3-optimizer/PopsicleV3Optimizer.sol:123-158
    address public immutable override token0;
    /// @inheritdoc IPopsicleV3Optimizer
    address public immutable override token1;
    // WETH address
    address public constant weth = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;
    // @inheritdoc IPopsicleV3Optimizer
    int24 public immutable override tickSpacing;

    uint24 constant GLOBAL_DIVISIONER = 1e6; // for basis point (0.0001%)
    //The protocol's fee in hundredths of a bip, i.e. 1e-6
    uint24 constant protocolFee = 2 * 1e5; //20%

    mapping (address => bool) private _operatorApproved;

    // @inheritdoc IPopsicleV3Optimizer
    IUniswapV3Pool public override pool;
    // Accrued protocol fees in terms of token0
    uint256 public protocolFees0;
    // Accrued protocol fees in terms of token1
    uint256 public protocolFees1;
    // Total lifetime accrued fees in terms of token0
    uint256 public totalFees0;
    // Total lifetime accrued fees in terms of token1
    uint256 public totalFees1;
    
    // Address of the Optimizer's owner
    address public governance;
    // Pending to claim ownership address
    address public pendingGovernance;
    //PopsicleV3 Optimizer settings address
    address public strategy;
    // Current tick lower of Optimizer pool position
    int24 public override tickLower;
    // Current tick higher of Optimizer pool position
    int24 public override tickUpper;
    // Checks if Optimizer is initialized

// Literal Solidity excerpt: contracts/22/contracts/popsicle-v3-optimizer/PopsicleV3Optimizer.sol:423-477
    function _earnFees() internal {
        uint liquidity = pool.positionLiquidity(tickLower, tickUpper);
        if (liquidity == 0) return; // we can't poke when liquidity is zero
         // Do zero-burns to poke the Uniswap pools so earned fees are updated
        pool.burn(tickLower, tickUpper, 0);
        
        (uint256 collect0, uint256 collect1) =
            pool.collect(
                address(this),
                tickLower,
                tickUpper,
                type(uint128).max,
                type(uint128).max
            );

        // Calculate protocol's fees
        uint256 earnedProtocolFees0 = collect0.mul(protocolFee).unsafeDiv(GLOBAL_DIVISIONER); //gadi ?
        uint256 earnedProtocolFees1 = collect1.mul(protocolFee).unsafeDiv(GLOBAL_DIVISIONER); //gadi ?
        protocolFees0 = protocolFees0.add(earnedProtocolFees0);
        protocolFees1 = protocolFees1.add(earnedProtocolFees1);
        totalFees0 = totalFees0.add(collect0);
        totalFees1 = totalFees1.add(collect1);
        emit CollectFees(collect0, collect1, totalFees0, totalFees1);
    }

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

// Literal Solidity excerpt: contracts/22/contracts/popsicle-v3-optimizer/PopsicleV3Optimizer.sol:570-600
    function collectProtocolFees(
        uint256 amount0,
        uint256 amount1
    ) external nonReentrant onlyGovernance {
        _earnFees();
        require(protocolFees0 >= amount0, "A0F");
        require(protocolFees1 >= amount1, "A1F");
        uint256 balance0 = IERC20(token0).balanceOf(address(this));
        uint256 balance1 = IERC20(token1).balanceOf(address(this));
        require(balance0 >= amount0 && balance1 >= amount1);
        if (amount0 > 0) pay(token0, address(this), msg.sender, amount0);
        if (amount1 > 0) pay(token1, address(this), msg.sender, amount1);
        
        protocolFees0 = protocolFees0.sub(amount0);
        protocolFees1 = protocolFees1.sub(amount1);
        _compoundFees();
        emit RewardPaid(msg.sender, amount0, amount1);
    }

    // Function modifier that checks if price has not moved a lot recently.
    // This mitigates price manipulation during rebalance and also prevents placing orders
    // when it's too volatile.
    modifier checkDeviation() {
    //    pool.checkDeviation(IOptimizerStrategy(strategy).maxTwapDeviation(), IOptimizerStrategy(strategy).twapDuration());
        _;
    }

    /**
     * @notice `setGovernance()` should be called by the existing governance
     * address prior to calling this function.
     */
