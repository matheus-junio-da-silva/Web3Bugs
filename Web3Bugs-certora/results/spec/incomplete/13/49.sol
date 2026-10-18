// Source: contracts/13/contracts/mocks/certora/ValuationHarness.sol
// Original lines: 164-196
    }

    function getifCashNetPresentValue(
        address account,
        uint256 blockTime,
        bool riskAdjusted
    ) external view returns (int256) {
        require(symbolicAccountContext.nextSettleTime >= blockTime);
        bytes32 assetsBitmap = BitmapAssetsHandler.getAssetsBitmap(
            account,
            symbolicAccountContext.bitmapCurrencyId
        );

        // prettier-ignore
        (int256 pv, /* hasDebt */) =
            BitmapAssetsHandler.getifCashNetPresentValue(
                account,
                symbolicAccountContext.bitmapCurrencyId,
                symbolicAccountContext.nextSettleTime,
                blockTime,
                assetsBitmap,
                symbolicCashGroup,
                riskAdjusted
            );

        return pv;
    }

    function getNumBitmapAssets(address account) external view returns (int256) {
        bytes32 assetsBitmap = BitmapAssetsHandler.getAssetsBitmap(
            account,
            symbolicAccountContext.bitmapCurrencyId
        );

// Source: contracts/13/contracts/mocks/certora/ValuationHarness.sol
// Original lines: 190-202
    }

    function getNumBitmapAssets(address account) external view returns (int256) {
        bytes32 assetsBitmap = BitmapAssetsHandler.getAssetsBitmap(
            account,
            symbolicAccountContext.bitmapCurrencyId
        );

        // Return int256 for comparison
        return int256(assetsBitmap.totalBitsSet());
    }
}
