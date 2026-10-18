// Source: contracts/13/contracts/internal/balances/BalanceHandler.sol
// Original lines: 1-35
// SPDX-License-Identifier: GPL-3.0-only
pragma solidity >0.7.0;
pragma experimental ABIEncoderV2;

import "./Incentives.sol";
import "./TokenHandler.sol";
import "../AccountContextHandler.sol";
import "../../global/Types.sol";
import "../../global/Constants.sol";
import "../../math/SafeInt256.sol";

library BalanceHandler {
    using SafeInt256 for int256;
    using TokenHandler for Token;
    using AssetRate for AssetRateParameters;
    using AccountContextHandler for AccountContext;

    /// @notice Emitted when a cash balance changes
    event CashBalanceChange(address indexed account, uint16 currencyId, int256 netCashChange);
    /// @notice Emitted when nToken supply changes (not the same as transfers)
    event nTokenSupplyChange(address indexed account, uint16 currencyId, int256 tokenSupplyChange);

    /// @notice Deposits asset tokens into an account
    /// @dev Handles two special cases when depositing tokens into an account.
    ///  - If a token has transfer fees then the amount specified does not equal the amount that the contract
    ///    will receive. Complete the deposit here rather than in finalize so that the contract has the correct
    ///    balance to work with.
    ///  - Force a transfer before finalize to allow a different account to deposit into an account
    /// @return Returns two values:
    ///  - assetAmountInternal which is the converted asset amount accounting for transfer fees
    ///  - assetAmountTransferred which is the internal precision amount transferred into the account
    function depositAssetToken(
        BalanceState memory balanceState,
        address account,
        int256 assetAmountExternal,

// Source: contracts/13/contracts/mocks/certora/AccountPortfolioHarness.sol
// Original lines: 78-110
    }

    function getCashBalance(address account, uint256 currencyId) public returns (int256) {
        // prettier-ignore
        (int256 cashBalance, /* */, /* */, /* */) = BalanceHandler.getBalanceStorage(account, currencyId);
        return cashBalance;
    }

    function getNTokenBalance(address account, uint256 currencyId) public returns (int256) {
        // prettier-ignore
        (/* */, int256 nTokenBalance, /* */, /* */) = BalanceHandler.getBalanceStorage(account, currencyId);
        return nTokenBalance;
    }

    function getLastClaimTime(address account, uint256 currencyId) public returns (uint256) {
        // prettier-ignore
        (/* */, /* */, uint256 lastClaimTime, /* */) = BalanceHandler.getBalanceStorage(account, currencyId);
        return lastClaimTime;
    }

    function getLastClaimSupply(address account, uint256 currencyId) public returns (uint256) {
        // prettier-ignore
        (/* */, /* */, /* */, uint256 lastClaimSupply) = BalanceHandler.getBalanceStorage(account, currencyId);
        return lastClaimSupply;
    }


    function getStoredAsset(address account, uint256 i) public view returns (uint256) {
        return symbolicPortfolioState.storedAssets[i].currencyId;
    }
    /** State Changing Methods **/

    function enableBitmapForAccount(
