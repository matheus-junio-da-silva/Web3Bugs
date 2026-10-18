// Historical target HAaveProtocolV2; exact Solidity excerpt
// Source: contracts/10/contracts/handlers/aavev2/HAaveProtocolV2.sol lines 1-70
// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "../../interface/IProxy.sol";
import "../HandlerBase.sol";
import "../wrappednativetoken/IWrappedNativeToken.sol";
import "./ILendingPoolV2.sol";
import "./IFlashLoanReceiver.sol";
import "./ILendingPoolAddressesProviderV2.sol";
import "./libraries/DataTypes.sol";

contract HAaveProtocolV2 is HandlerBase, IFlashLoanReceiver {
    using SafeERC20 for IERC20;

    uint16 public constant REFERRAL_CODE = 56;
    address public immutable provider;
    address public immutable wrappedNativeToken;

    constructor(address wrappedNativeToken_, address provider_) {
        wrappedNativeToken = wrappedNativeToken_;
        provider = provider_;
    }

    function getContractName() public pure override returns (string memory) {
        return "HAaveProtocolV2";
    }

    function deposit(
        address asset,
        uint256 amount
    ) external payable returns (uint256 depositAmount) {
        amount = _getBalance(asset, amount);
        depositAmount = _deposit(asset, amount);
    }

    function depositETH(
        uint256 amount
    ) external payable returns (uint256 depositAmount) {
        amount = _getBalance(NATIVE_TOKEN_ADDRESS, amount);
        IWrappedNativeToken(wrappedNativeToken).deposit{value: amount}();
        depositAmount = _deposit(wrappedNativeToken, amount);

        _updateToken(wrappedNativeToken);
    }

    function withdraw(
        address asset,
        uint256 amount
    ) external payable returns (uint256 withdrawAmount) {
        withdrawAmount = _withdraw(asset, amount);

        _updateToken(asset);
    }

    function withdrawETH(
        uint256 amount
    ) external payable returns (uint256 withdrawAmount) {
        withdrawAmount = _withdraw(wrappedNativeToken, amount);
        IWrappedNativeToken(wrappedNativeToken).withdraw(withdrawAmount);
    }

    function repay(
        address asset,
        uint256 amount,
        uint256 rateMode,
        address onBehalfOf
    ) external payable returns (uint256 remainDebt) {
        remainDebt = _repay(asset, amount, rateMode, onBehalfOf);

// Exact original source contracts/10/contracts/handlers/aavev2/HAaveProtocolV2.sol:100-143
    function flashLoan(
        address[] calldata assets,
        uint256[] calldata amounts,
        uint256[] calldata modes,
        bytes calldata params
    ) external payable {
        _requireMsg(
            assets.length == amounts.length,
            "flashLoan",
            "assets and amounts do not match"
        );

        _requireMsg(
            assets.length == modes.length,
            "flashLoan",
            "assets and modes do not match"
        );

        address onBehalfOf = _getSender();
        address pool = ILendingPoolAddressesProviderV2(provider)
            .getLendingPool();

        try
            ILendingPoolV2(pool).flashLoan(
                address(this),
                assets,
                amounts,
                modes,
                onBehalfOf,
                params,
                REFERRAL_CODE
            )
        {} catch Error(string memory reason) {
            _revertMsg("flashLoan", reason);
        } catch {
            _revertMsg("flashLoan");
        }

        // approve lending pool zero
        for (uint256 i = 0; i < assets.length; i++) {
            _tokenApproveZero(assets[i], pool);
            if (modes[i] != 0) _updateToken(assets[i]);
        }
    }
