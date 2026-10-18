// Exact Solidity excerpt for HCurve
// Source: contracts/10/contracts/handlers/curve/HCurve.sol original lines 1-70
// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "../HandlerBase.sol";
import "./ICurveHandler.sol";

contract HCurve is HandlerBase {
    using SafeERC20 for IERC20;

    function getContractName() public pure override returns (string memory) {
        return "HCurve";
    }

    /// @notice Curve exchange
    function exchange(
        address handler,
        address tokenI,
        address tokenJ,
        int128 i,
        int128 j,
        uint256 amount,
        uint256 minAmount
    ) external payable returns (uint256) {
        (
            uint256 _amount,
            uint256 balanceBefore,
            uint256 ethAmount
        ) = _exchangeBefore(handler, tokenI, tokenJ, amount);
        try
            ICurveHandler(handler).exchange{value: ethAmount}(
                i,
                j,
                _amount,
                minAmount
            )
        {} catch Error(string memory reason) {
            _revertMsg("exchange", reason);
        } catch {
            _revertMsg("exchange");
        }

        return _exchangeAfter(handler, tokenI, tokenJ, balanceBefore);
    }

    /// @notice Curve exchange with uint256 ij
    function exchangeUint256(
        address handler,
        address tokenI,
        address tokenJ,
        uint256 i,
        uint256 j,
        uint256 amount,
        uint256 minAmount
    ) external payable returns (uint256) {
        (
            uint256 _amount,
            uint256 balanceBefore,
            uint256 ethAmount
        ) = _exchangeBefore(handler, tokenI, tokenJ, amount);
        try
            ICurveHandler(handler).exchange{value: ethAmount}(
                i,
                j,
                _amount,
                minAmount
            )
        {} catch Error(string memory reason) {
            _revertMsg("exchangeUint256", reason);

// Exact original Solidity: contracts/10/contracts/handlers/curve/HCurve.sol lines 246-344
    function addLiquidity(
        address handler,
        address pool,
        address[] calldata tokens,
        uint256[] calldata amounts,
        uint256 minPoolAmount
    ) external payable returns (uint256) {
        (
            uint256[] memory _amounts,
            uint256 balanceBefore,
            uint256 ethAmount
        ) = _addLiquidityBefore(handler, pool, tokens, amounts);

        // Execute add_liquidity according to amount array size
        if (_amounts.length == 2) {
            uint256[2] memory amts = [_amounts[0], _amounts[1]];
            try
                ICurveHandler(handler).add_liquidity{value: ethAmount}(
                    amts,
                    minPoolAmount
                )
            {} catch Error(string memory reason) {
                _revertMsg("addLiquidity", reason);
            } catch {
                _revertMsg("addLiquidity");
            }
        } else if (_amounts.length == 3) {
            uint256[3] memory amts = [_amounts[0], _amounts[1], _amounts[2]];
            try
                ICurveHandler(handler).add_liquidity{value: ethAmount}(
                    amts,
                    minPoolAmount
                )
            {} catch Error(string memory reason) {
                _revertMsg("addLiquidity", reason);
            } catch {
                _revertMsg("addLiquidity");
            }
        } else if (_amounts.length == 4) {
            uint256[4] memory amts = [
                _amounts[0],
                _amounts[1],
                _amounts[2],
                _amounts[3]
            ];
            try
                ICurveHandler(handler).add_liquidity{value: ethAmount}(
                    amts,
                    minPoolAmount
                )
            {} catch Error(string memory reason) {
                _revertMsg("addLiquidity", reason);
            } catch {
                _revertMsg("addLiquidity");
            }
        } else if (_amounts.length == 5) {
            uint256[5] memory amts = [
                _amounts[0],
                _amounts[1],
                _amounts[2],
                _amounts[3],
                _amounts[4]
            ];
            try
                ICurveHandler(handler).add_liquidity{value: ethAmount}(
                    amts,
                    minPoolAmount
                )
            {} catch Error(string memory reason) {
                _revertMsg("addLiquidity", reason);
            } catch {
                _revertMsg("addLiquidity");
            }
        } else if (_amounts.length == 6) {
            uint256[6] memory amts = [
                _amounts[0],
                _amounts[1],
                _amounts[2],
                _amounts[3],
                _amounts[4],
                _amounts[5]
            ];
            try
                ICurveHandler(handler).add_liquidity{value: ethAmount}(
                    amts,
                    minPoolAmount
                )
            {} catch Error(string memory reason) {
                _revertMsg("addLiquidity", reason);
            } catch {
                _revertMsg("addLiquidity");
            }
        } else {
            _revertMsg("addLiquidity", "invalid amount[] size");
        }

        return
            _addLiquidityAfter(handler, pool, tokens, amounts, balanceBefore);
    }
