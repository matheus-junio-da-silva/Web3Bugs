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

// Literal Solidity excerpt: contracts/22/spec/harness/DummyERC20A.sol:4-45
contract DummyERC20A is IERC20 {
    using SafeMath for uint256;

    uint256 supply;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowances;

    string public name;
    string public symbol;
    uint public decimals;

    function totalSupply() external view override returns (uint256) {
        return supply;
    }
    function balanceOf(address account) external view override returns (uint256) {
        return balances[account];
    }
    function transfer(address recipient, uint256 amount) external override returns (bool) {
        balances[msg.sender] = balances[msg.sender].sub(amount);
        balances[recipient] = balances[recipient].add(amount);
        return true;
    }

    function allowance(address owner, address spender) external view override returns (uint256) {
        return allowances[owner][spender];
    }

    function approve(address spender, uint256 amount) external override returns (bool) {
        allowances[msg.sender][spender] = amount;
        return true;
    }

    function transferFrom(
        address sender,
        address recipient,
        uint256 amount
    ) external override returns (bool) {
        balances[sender] = balances[sender].sub(amount);
        balances[recipient] = balances[recipient].add(amount);
        allowances[sender][msg.sender] = allowances[sender][msg.sender].sub(amount);
        return true;
    }
