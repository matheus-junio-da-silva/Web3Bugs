// Project 10 example 242; handler HSushiSwap, property noOverwrite. Historical source excerpts only, NOT compilable assembly.
// Source: contracts/10/contracts/handlers/sushiswap/HSushiSwap.sol original lines 22-47
    }

    function addLiquidityETH(
        uint256 value,
        address token,
        uint256 amountTokenDesired,
        uint256 amountTokenMin,
        uint256 amountETHMin
    )
        external
        payable
        returns (uint256 amountToken, uint256 amountETH, uint256 liquidity)
    {
        // Get uniswapV2 router
        IUniswapV2Router02 router = IUniswapV2Router02(sushiSwapRouter);

        // Approve token
        value = _getBalance(address(0), value);
        amountTokenDesired = _getBalance(token, amountTokenDesired);
        _tokenApprove(token, sushiSwapRouter, amountTokenDesired);

        // Add liquidity ETH
        try
            router.addLiquidityETH{value: value}(
                token,
                amountTokenDesired,

// Source: contracts/10/contracts/handlers/sushiswap/HSushiSwap.sol original lines 71-96
    }

    function addLiquidity(
        address tokenA,
        address tokenB,
        uint256 amountADesired,
        uint256 amountBDesired,
        uint256 amountAMin,
        uint256 amountBMin
    )
        external
        payable
        returns (uint256 amountA, uint256 amountB, uint256 liquidity)
    {
        // Get uniswapV2 router
        IUniswapV2Router02 router = IUniswapV2Router02(sushiSwapRouter);

        // Approve token
        amountADesired = _getBalance(tokenA, amountADesired);
        amountBDesired = _getBalance(tokenB, amountBDesired);
        _tokenApprove(tokenA, sushiSwapRouter, amountADesired);
        _tokenApprove(tokenB, sushiSwapRouter, amountBDesired);

        // Add liquidity
        try
            router.addLiquidity(

// Source: contracts/10/specs/harnesses/ProxyHarness.sol original lines 7-25 (literal excerpt)

    function getSlot(uint256 s) external view returns (uint256 x) {
        assembly {
            x := sload(s)
        }
    }

    function getStackLengthSlot() external view returns (uint256 x) {
        assembly {
            x := stack_slot
        }
    }

    function getStackLength() external view returns (uint256) {
        return stack.length;
    }

    function ethBalance(address who) external view returns (uint256) {
        return who.balance;
