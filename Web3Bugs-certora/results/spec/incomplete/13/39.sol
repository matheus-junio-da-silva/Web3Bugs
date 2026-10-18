// Source: contracts/13/contracts/mocks/certora/SettlementHarness.sol
// Original lines: 21-53
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
    }

    function getNumSettleableAssets(address account, uint256 blockTime)
        external

// Source: contracts/13/contracts/mocks/certora/SettlementHarness.sol
// Original lines: 90-118
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
    }
}
