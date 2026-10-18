// Historical target HSCompound; exact Solidity excerpt
// Source: contracts/10/contracts/handlers/compound/HSCompound.sol lines 1-70
// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

import "../HandlerBase.sol";
import "../maker/IDSProxy.sol";
import "./ICToken.sol";
import "./IComptroller.sol";

contract HSCompound is HandlerBase {
    using SafeERC20 for IERC20;

    // prettier-ignore
    address public constant FCOMPOUND_ACTIONS = 0x05EF8eb657027927fAB9b279138f0189CB144976;
    // prettier-ignore
    address public constant COMPTROLLER = 0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3B;
    // prettier-ignore
    address public constant CETH_ADDRESS = 0x4Ddc2D193948926D02f9B1fE9e1daa0718270ED5;
    // prettier-ignore
    address public constant COMP_ADDRESS = 0xc00e94Cb662C3520282E6f5717214004A7f26888;

    function getContractName() public pure override returns (string memory) {
        return "HSCompound";
    }

    modifier isDSProxyOwner(address dsProxy) {
        address sender = _getSender();
        _requireMsg(
            IDSProxy(dsProxy).owner() == sender,
            "General",
            "Not owner of the DSProxy"
        );
        _;
    }

    function deposit(
        address dsProxy,
        address token,
        uint256 amount
    ) external payable isDSProxyOwner(dsProxy) {
        _deposit(dsProxy, token, amount);
    }

    function withdraw(
        address dsProxy,
        address token,
        uint256 amount
    ) external payable isDSProxyOwner(dsProxy) {
        _withdraw(dsProxy, token, amount);
        if (token != NATIVE_TOKEN_ADDRESS) _updateToken(token);
    }

    function borrow(
        address dsProxy,
        address cTokenIn,
        address cTokenBorrow,
        uint256 cAmountIn,
        uint256 uBorrowAmount,
        bool needEnterMarket
    ) external payable isDSProxyOwner(dsProxy) {
        if (cAmountIn > 0) {
            _deposit(dsProxy, cTokenIn, cAmountIn);
        }

        if (needEnterMarket) {
            _enterMarket(dsProxy, cTokenIn);
        }

