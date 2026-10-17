// Source: contracts/13/contracts/mocks/certora/ValuationHarness.sol
// Original lines: 120-152
    }

    function checkPortfolioSorted(address account) external view returns (bool) {
        PortfolioAsset[] memory assets = PortfolioHandler.getSortedPortfolio(
            account,
            symbolicAccountContext.assetArrayLength
        );
        for (uint256 i; i < assets.length; i++) {
            if (i == 0) continue;
            assert(assets[i - 1].currencyId <= assets[i].currencyId);
            assert(assets[i - 1].maturity <= assets[i].maturity);
            assert(assets[i - 1].assetType <= assets[i].assetType);
        }
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