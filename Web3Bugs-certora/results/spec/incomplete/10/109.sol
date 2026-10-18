// Exact Solidity excerpt for HSushiSwap
// Source: contracts/10/contracts/handlers/sushiswap/HSushiSwap.sol original lines 1-70
// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

import "../HandlerBase.sol";
import "./libraries/SushiSwapLibrary.sol";
import "../uniswapv2/IUniswapV2Router02.sol";

contract HSushiSwap is HandlerBase {
    using SafeERC20 for IERC20;

    address public immutable sushiSwapRouter;

    constructor(address sushiSwapRouter_) {
        sushiSwapRouter = sushiSwapRouter_;
    }

    function getContractName() public pure override returns (string memory) {
        return "HSushiSwap";
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
                amountTokenMin,
                amountETHMin,
                address(this),
                block.timestamp
            )
        returns (uint256 ret1, uint256 ret2, uint256 ret3) {
            amountToken = ret1;
            amountETH = ret2;
            liquidity = ret3;
        } catch Error(string memory reason) {
            _revertMsg("addLiquidityETH", reason);
        } catch {
            _revertMsg("addLiquidityETH");
        }
        _tokenApproveZero(token, sushiSwapRouter);

        // Update involved token
        address pair = SushiSwapLibrary.pairFor(
            router.factory(),
            token,
            router.WETH()
        );
        _updateToken(pair);
