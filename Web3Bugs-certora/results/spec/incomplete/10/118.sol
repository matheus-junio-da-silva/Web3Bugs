// Exact Solidity excerpt for HUniswapV2
// Source: contracts/10/contracts/handlers/uniswapv2/HUniswapV2.sol original lines 1-70
// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

import "../HandlerBase.sol";
import "./libraries/UniswapV2Library.sol";
import "./IUniswapV2Router02.sol";

contract HUniswapV2 is HandlerBase {
    using SafeERC20 for IERC20;

    // prettier-ignore
    address public constant UNISWAPV2_ROUTER = 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D;

    function getContractName() public pure override returns (string memory) {
        return "HUniswapV2";
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
        IUniswapV2Router02 router = IUniswapV2Router02(UNISWAPV2_ROUTER);

        // Approve token
        value = _getBalance(address(0), value);
        amountTokenDesired = _getBalance(token, amountTokenDesired);
        _tokenApprove(token, UNISWAPV2_ROUTER, amountTokenDesired);

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
        _tokenApproveZero(token, UNISWAPV2_ROUTER);

        // Update involved token
        address pair = UniswapV2Library.pairFor(
            router.factory(),
            token,
            router.WETH()
        );
        _updateToken(pair);
    }

    function addLiquidity(

// Verbatim source contracts/10/contracts/handlers/uniswapv2/HUniswapV2.sol:70-122
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
        IUniswapV2Router02 router = IUniswapV2Router02(UNISWAPV2_ROUTER);

        // Approve token
        amountADesired = _getBalance(tokenA, amountADesired);
        amountBDesired = _getBalance(tokenB, amountBDesired);
        _tokenApprove(tokenA, UNISWAPV2_ROUTER, amountADesired);
        _tokenApprove(tokenB, UNISWAPV2_ROUTER, amountBDesired);

        // Add liquidity
        try
            router.addLiquidity(
                tokenA,
                tokenB,
                amountADesired,
                amountBDesired,
                amountAMin,
                amountBMin,
                address(this),
                block.timestamp
            )
        returns (uint256 ret1, uint256 ret2, uint256 ret3) {
            amountA = ret1;
            amountB = ret2;
            liquidity = ret3;
        } catch Error(string memory reason) {
            _revertMsg("addLiquidity", reason);
        } catch {
            _revertMsg("addLiquidity");
        }
        _tokenApproveZero(tokenA, UNISWAPV2_ROUTER);
        _tokenApproveZero(tokenB, UNISWAPV2_ROUTER);

        // Update involved token
        address pair = UniswapV2Library.pairFor(
            router.factory(),
            tokenA,
            tokenB
        );
        _updateToken(pair);
    }

// Verbatim source contracts/10/contracts/handlers/uniswapv2/HUniswapV2.sol:166-209
    function removeLiquidity(
        address tokenA,
        address tokenB,
        uint256 liquidity,
        uint256 amountAMin,
        uint256 amountBMin
    ) external payable returns (uint256 amountA, uint256 amountB) {
        // Get uniswapV2 router
        IUniswapV2Router02 router = IUniswapV2Router02(UNISWAPV2_ROUTER);
        address pair = UniswapV2Library.pairFor(
            router.factory(),
            tokenA,
            tokenB
        );

        // Approve token
        liquidity = _getBalance(pair, liquidity);
        _tokenApprove(pair, UNISWAPV2_ROUTER, liquidity);

        // remove liquidity
        try
            router.removeLiquidity(
                tokenA,
                tokenB,
                liquidity,
                amountAMin,
                amountBMin,
                address(this),
                block.timestamp
            )
        returns (uint256 ret1, uint256 ret2) {
            amountA = ret1;
            amountB = ret2;
        } catch Error(string memory reason) {
            _revertMsg("removeLiquidity", reason);
        } catch {
            _revertMsg("removeLiquidity");
        }
        _tokenApproveZero(pair, UNISWAPV2_ROUTER);

        // Update involved token
        _updateToken(tokenA);
        _updateToken(tokenB);
    }
