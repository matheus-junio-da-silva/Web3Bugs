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
