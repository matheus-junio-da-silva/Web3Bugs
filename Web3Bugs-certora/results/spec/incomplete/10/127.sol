// Exact Solidity excerpt for HYVault
// Source: contracts/10/contracts/handlers/yearn/HYVault.sol original lines 1-70
// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "../HandlerBase.sol";
import "./IYVault.sol";

contract HYVault is HandlerBase {
    using SafeERC20 for IERC20;

    function getContractName() public pure override returns (string memory) {
        return "HYVault";
    }

    function deposit(
        address vault,
        uint256 _amount
    ) external payable returns (uint256) {
        IYVault yVault = IYVault(vault);
        uint256 beforeYTokenBalance = IERC20(address(yVault)).balanceOf(
            address(this)
        );

        address token = yVault.token();
        // if amount == type(uint256).max return balance of Proxy
        _amount = _getBalance(token, _amount);
        _tokenApprove(token, address(yVault), _amount);
        try yVault.deposit(_amount) {} catch Error(string memory reason) {
            _revertMsg("deposit", reason);
        } catch {
            _revertMsg("deposit");
        }
        _tokenApproveZero(token, address(yVault));

        uint256 afterYTokenBalance = IERC20(address(yVault)).balanceOf(
            address(this)
        );

        _updateToken(address(yVault));
        return afterYTokenBalance - beforeYTokenBalance;
    }

    function depositETH(
        uint256 value,
        address vault
    ) external payable returns (uint256) {
        IYVault yVault = IYVault(vault);
        uint256 beforeYTokenBalance = IERC20(address(yVault)).balanceOf(
            address(this)
        );
        // if amount == type(uint256).max return balance of Proxy
        value = _getBalance(address(0), value);
        try yVault.depositETH{value: value}() {} catch Error(
            string memory reason
        ) {
            _revertMsg("depositETH", reason);
        } catch {
            _revertMsg("depositETH");
        }
        uint256 afterYTokenBalance = IERC20(address(yVault)).balanceOf(
            address(this)
        );

        _updateToken(address(yVault));
        return afterYTokenBalance - beforeYTokenBalance;
    }

    function withdraw(
        address vault,
