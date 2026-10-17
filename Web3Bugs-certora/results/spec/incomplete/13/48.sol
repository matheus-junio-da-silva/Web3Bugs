// Source: contracts/13/contracts/mocks/certora/ValuationHarness.sol
// Original lines: 133-165
    }

    function getPortfolioCurrencyIdAtIndex(address account, uint256 index)
        external
        view
        returns (uint256)
    {
        PortfolioAsset[] memory assets = PortfolioHandler.getSortedPortfolio(
            account,
            symbolicAccountContext.assetArrayLength
        );
        return assets[index].currencyId;
    }

    function getNetCashGroupValue(
        address account,
        uint256 portfolioIndex,
        uint256 blockTime
    ) external view returns (int256, uint256) {
        PortfolioAsset[] memory assets = PortfolioHandler.getSortedPortfolio(
            account,
            symbolicAccountContext.assetArrayLength
        );
        return
            AssetHandler.getNetCashGroupValue(
                assets,
                symbolicCashGroup,
                symbolicMarket,
                blockTime,
                portfolioIndex
            );
    }


// Source: contracts/13/contracts/mocks/certora/ValuationHarness.sol
// Original lines: 145-177
    }

    function getNetCashGroupValue(
        address account,
        uint256 portfolioIndex,
        uint256 blockTime
    ) external view returns (int256, uint256) {
        PortfolioAsset[] memory assets = PortfolioHandler.getSortedPortfolio(
            account,
            symbolicAccountContext.assetArrayLength
        );
        return
            AssetHandler.getNetCashGroupValue(
                assets,
                symbolicCashGroup,
                symbolicMarket,
                blockTime,
                portfolioIndex
            );
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