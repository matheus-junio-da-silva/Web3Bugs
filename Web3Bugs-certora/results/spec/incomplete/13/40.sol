// Source: contracts/13/contracts/mocks/certora/SettlementHarness.sol
// Original lines: 17-49
    PortfolioState symbolicPortfolioState;

    function getBitmapCurrencyId(address account) external view returns (uint256) {
        return symbolicAccountContext.bitmapCurrencyId;
    }

    function getSettlementRate(uint256 currencyId, uint256 maturity)
        external
        view
        returns (int256)
    {
        AssetRateParameters memory ar = AssetRate.buildSettlementRateView(currencyId, maturity);
        return ar.rate;
    }

    function getCashBalance(address account, uint256 currencyId) external view returns (int256) {
        BalanceState memory balanceState;
        BalanceHandler.loadBalanceState(balanceState, account, currencyId, symbolicAccountContext);

        return balanceState.storedCashBalance;
    }

    function _getAccountAssets(address account) internal view returns (PortfolioAsset[] memory) {
        if (symbolicAccountContext.bitmapCurrencyId == 0) {
            return symbolicPortfolioState.storedAssets;
        } else {
            return
                BitmapAssetsHandler.getifCashArray(
                    account,
                    symbolicAccountContext.bitmapCurrencyId,
                    symbolicAccountContext.nextSettleTime
                );
        }

// Source: contracts/13/contracts/mocks/certora/SettlementHarness.sol
// Original lines: 50-82
    }

    function getNumSettleableAssets(address account, uint256 blockTime)
        external
        view
        returns (uint256)
    {
        uint256 numSettleableAssets;
        PortfolioAsset[] memory assets = _getAccountAssets(account);

        for (uint256 i; i < assets.length; i++) {
            if (assets[i].getSettlementDate() <= blockTime) numSettleableAssets++;
        }

        return numSettleableAssets;
    }

    function getAmountToSettle(
        uint256 currencyId,
        address account,
        uint256 blockTime
    ) external view returns (int256) {
        int256 amountToSettle;
        PortfolioAsset[] memory assets = _getAccountAssets(account);

        for (uint256 i; i < assets.length; i++) {
            // TODO: incomplete, but is this even the right approach?
            if (assets[i].getSettlementDate() <= blockTime && assets[i].currencyId == currencyId) {
                // AssetRate memory ar = AssetRate.buildSettlementRateView(currencyId, maturity);
            }
        }

        return amountToSettle;
// Source: contracts/13/contracts/mocks/certora/SettlementHarness.sol
// Original lines: 83-115
    }

    function getNumAssets(address account) external view returns (uint256) {
        PortfolioAsset[] memory assets = _getAccountAssets(account);
        // Value of any asset should never be zero. If it is then it should not exist in the portfolio.
        for (uint256 i; i < assets.length; i++) assert(assets[i].notional != 0);
        return assets.length;
    }

    function settleAccount(address account) external {
        // This is an approximation of what happens in SettleAssetsExternal._settleAccount
        SettleAmount[] memory settleAmounts;

        if (symbolicAccountContext.bitmapCurrencyId != 0) {
            settleAmounts = SettleAssetsExternal._settleBitmappedAccountStateful(
                account,
                symbolicAccountContext.bitmapCurrencyId,
                symbolicAccountContext.nextSettleTime
            );
        } else {
            settleAmounts = SettlePortfolioAssets.settlePortfolio(
                symbolicPortfolioState,
                block.timestamp
            );

            symbolicAccountContext.storeAssetsAndUpdateContext(
                account,
                symbolicPortfolioState,
                false
            );
        }

        BalanceHandler.finalizeSettleAmounts(account, symbolicAccountContext, settleAmounts);
