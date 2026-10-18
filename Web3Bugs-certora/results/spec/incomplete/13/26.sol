// Source: contracts/13/contracts/mocks/certora/GetterSetterHarness.sol
// Original lines: 9-41
    using AccountContextHandler for AccountContext;

    function setAccountContext(
        address account,
        uint40 nextSettleTime,
        uint8 hasDebt,
        uint8 assetArrayLength,
        uint16 bitmapCurrencyId,
        uint144 activeCurrencies
    ) external {
        AccountContext memory accountContext =
            AccountContext({
                nextSettleTime: nextSettleTime,
                hasDebt: bytes1(hasDebt),
                assetArrayLength: assetArrayLength,
                bitmapCurrencyId: bitmapCurrencyId,
                activeCurrencies: bytes18(activeCurrencies)
            });
        accountContext.setAccountContext(account);
    }

    function getAccountContext(address account) external view returns (AccountContext memory) {
        return AccountContextHandler.getAccountContext(account);
    }

    // TODO: remove these once we can handle bytesNN natively
    function getNextSettleTime(address account) external view returns (uint40) {
        return AccountContextHandler.getAccountContext(account).nextSettleTime;
    }

    function getHasDebt(address account) external view returns (uint8) {
        return uint8(AccountContextHandler.getAccountContext(account).hasDebt);
    }

// Source: contracts/13/contracts/mocks/certora/GetterSetterHarness.sol
// Original lines: 33-55

    // TODO: remove these once we can handle bytesNN natively
    function getNextSettleTime(address account) external view returns (uint40) {
        return AccountContextHandler.getAccountContext(account).nextSettleTime;
    }

    function getHasDebt(address account) external view returns (uint8) {
        return uint8(AccountContextHandler.getAccountContext(account).hasDebt);
    }

    function getAssetArrayLength(address account) external view returns (uint8) {
        return AccountContextHandler.getAccountContext(account).assetArrayLength;
    }

    function getBitmapCurrency(address account) external view returns (uint16) {
        return AccountContextHandler.getAccountContext(account).bitmapCurrencyId;
    }

    function getActiveCurrencies(address account) external view returns (uint144) {
        return uint144(AccountContextHandler.getAccountContext(account).activeCurrencies);
    }
}


// Source: contracts/13/contracts/internal/AccountContextHandler.sol
// Original lines: 33-65

    /// @notice Sets the account context of a given account
    function setAccountContext(AccountContext memory accountContext, address account) internal {
        bytes32 slot = keccak256(abi.encode(account, Constants.ACCOUNT_CONTEXT_STORAGE_OFFSET));
        bytes32 data =
            (bytes32(uint256(accountContext.nextSettleTime)) |
                (bytes32(accountContext.hasDebt) >> 208) |
                (bytes32(uint256(accountContext.assetArrayLength)) << 48) |
                (bytes32(uint256(accountContext.bitmapCurrencyId)) << 56) |
                (bytes32(accountContext.activeCurrencies) >> 40));

        assembly {
            sstore(slot, data)
        }

        emit AccountContextUpdate(account);
    }

    /// @notice Sets the account context of a given account
    function enableBitmapForAccount(
        AccountContext memory accountContext,
        address account,
        uint256 currencyId,
        uint256 blockTime
    ) internal view {
        // Allow setting the currency id to zero to turn off bitmap
        require(currencyId <= Constants.MAX_CURRENCIES, "AC: invalid currency id");

        if (accountContext.bitmapCurrencyId == 0) {
            require(accountContext.assetArrayLength == 0, "AC: cannot have assets");
            // Account context also cannot have negative cash debts
            require(accountContext.hasDebt == 0x00, "AC: cannot have debt");
