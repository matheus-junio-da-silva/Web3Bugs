// Historical target HFunds; exact Solidity excerpt
// Source: contracts/10/contracts/handlers/funds/HFunds.sol lines 1-70
// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "../../lib/LibFeeStorage.sol";
import "../HandlerBase.sol";

contract HFunds is HandlerBase {
    using SafeERC20 for IERC20;
    using LibFeeStorage for mapping(bytes32 => bytes32);

    event ChargeFee(address indexed tokenIn, uint256 feeAmount);

    function getContractName() public pure override returns (string memory) {
        return "HFunds";
    }

    function updateTokens(
        address[] calldata tokens
    ) external payable returns (uint256[] memory) {
        uint256[] memory balances = new uint256[](tokens.length);
        for (uint256 i = 0; i < tokens.length; ) {
            address token = tokens[i];
            if (token != address(0) && token != NATIVE_TOKEN_ADDRESS) {
                // Update involved token
                _updateToken(token);
            }
            balances[i] = _getBalance(token, type(uint256).max);
            unchecked {
                ++i;
            }
        }
        return balances;
    }

    function inject(
        address[] calldata tokens,
        uint256[] calldata amounts
    ) external payable returns (uint256[] memory) {
        return _inject(tokens, amounts);
    }

    // Same as inject() and just to make another interface for different use case
    function addFunds(
        address[] calldata tokens,
        uint256[] calldata amounts
    ) external payable returns (uint256[] memory) {
        return _inject(tokens, amounts);
    }

    function sendTokens(
        address[] calldata tokens,
        uint256[] calldata amounts,
        address payable receiver
    ) external payable {
        for (uint256 i = 0; i < tokens.length; ) {
            uint256 amount = _getBalance(tokens[i], amounts[i]);
            if (amount > 0) {
                // ETH case
                if (
                    tokens[i] == address(0) || tokens[i] == NATIVE_TOKEN_ADDRESS
                ) {
                    (bool success, ) = receiver.call{value: amount}("");
                    _requireMsg(success, "sendTokens", "failed to send Ether");
                } else {
                    IERC20(tokens[i]).safeTransfer(receiver, amount);
                }
            }
            unchecked {

// Exact original source contracts/10/contracts/handlers/funds/HFunds.sol:120-129
    function sendToken(
        address token,
        uint256 amount,
        address receiver
    ) external payable {
        amount = _getBalance(token, amount);
        if (amount > 0) {
            IERC20(token).safeTransfer(receiver, amount);
        }
    }

// Exact original source contracts/10/contracts/handlers/funds/HFunds.sol:52-74
    function sendTokens(
        address[] calldata tokens,
        uint256[] calldata amounts,
        address payable receiver
    ) external payable {
        for (uint256 i = 0; i < tokens.length; ) {
            uint256 amount = _getBalance(tokens[i], amounts[i]);
            if (amount > 0) {
                // ETH case
                if (
                    tokens[i] == address(0) || tokens[i] == NATIVE_TOKEN_ADDRESS
                ) {
                    (bool success, ) = receiver.call{value: amount}("");
                    _requireMsg(success, "sendTokens", "failed to send Ether");
                } else {
                    IERC20(tokens[i]).safeTransfer(receiver, amount);
                }
            }
            unchecked {
                ++i;
            }
        }
    }
