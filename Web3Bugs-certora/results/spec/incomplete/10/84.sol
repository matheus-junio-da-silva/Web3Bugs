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
