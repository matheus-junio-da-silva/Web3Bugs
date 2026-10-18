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

// Literal Solidity excerpt: contracts/22/contracts/popsicle-v3-optimizer/libraries/PoolActions.sol:1-83
// SPDX-License-Identifier: Unlicense

pragma solidity 0.7.6;
pragma abicoder v2;

import '../interfaces/IUniswapV3Pool.sol';
import './PoolVariables.sol';
import "./SafeCast.sol";
/// @title This library is created to conduct a variety of burn liquidity methods
library PoolActions {
    using PoolVariables for IUniswapV3Pool;
    using LowGasSafeMath for uint256;
    using SafeCast for uint256;

    /**
     * @notice Withdraws liquidity in share proportion to the Optimizer's totalSupply.
     * @param pool Uniswap V3 pool
     * @param tickLower The lower tick of the range
     * @param tickUpper The upper tick of the range
     * @param totalSupply The amount of total shares in existence
     * @param share to burn
     * @param to Recipient of amounts
     * @return amount0 Amount of token0 withdrawed
     * @return amount1 Amount of token1 withdrawed
     */
 function burnLiquidityShare(
        IUniswapV3Pool pool,
        int24 tickLower,
        int24 tickUpper,
        uint256 totalSupply,
        uint256 share,
        address to
    ) internal returns (uint256 amount0, uint256 amount1) {
        require(totalSupply > 0, "TS");
        uint128 liquidityInPool = pool.positionLiquidity(tickLower, tickUpper);
        uint256 liquidity = uint256(liquidityInPool).mul(share) / totalSupply;
        
        require ((liquidity < 2**128) && (totalSupply < 2**128));
        require (share == liquidity * totalSupply/uint256(liquidityInPool));

        if (liquidity > 0) {
            (amount0, amount1) = pool.burn(tickLower, tickUpper, liquidity.toUint128());

            if (amount0 > 0 || amount1 > 0) {
            // collect liquidity share
                (amount0, amount1) = pool.collect(
                    to,
                    tickLower,
                    tickUpper,
                    amount0.toUint128(),
                    amount1.toUint128()
                );
            }
        }
    }
    /**
     * @notice Withdraws all liquidity in a range from Uniswap pool
     * @param pool Uniswap V3 pool
     * @param tickLower The lower tick of the range
     * @param tickUpper The upper tick of the range
     */
    function burnAllLiquidity(
        IUniswapV3Pool pool,
        int24 tickLower,
        int24 tickUpper
    ) internal {
        
        // Burn all liquidity in this range
        uint128 liquidity = pool.positionLiquidity(tickLower, tickUpper);
        if (liquidity > 0) {
            pool.burn(tickLower, tickUpper, liquidity);
        }
        
         // Collect all owed tokens
        pool.collect(
            address(this),
            tickLower,
            tickUpper,
            type(uint128).max,
            type(uint128).max
        );
    }
}
