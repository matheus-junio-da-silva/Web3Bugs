// Source: contracts/13/contracts/mocks/certora/AccountPortfolioHarness.sol
// Original lines: 24-56
    }

    function getHasDebt(address account) external view returns (uint8) {
        return uint8(symbolicAccountContext.hasDebt);
    }

    function getAssetArrayLength(address account) external view returns (uint8) {
        return symbolicAccountContext.assetArrayLength;
    }

    function getBitmapCurrency(address account) external view returns (uint16) {
        return symbolicAccountContext.bitmapCurrencyId;
    }

    function getActiveCurrencies(address account) external view returns (uint144) {
        return uint144(symbolicAccountContext.activeCurrencies);
    }

    function getAssetsBitmap(address account) external view returns (uint256) {
        AccountContext memory accountContext = symbolicAccountContext;
        return
            uint256(BitmapAssetsHandler.getAssetsBitmap(account, accountContext.bitmapCurrencyId));
    }

    function getAccountContext(address account) external view returns (AccountContext memory) {
        return symbolicAccountContext;
    }

    // This is just a harness for getting the settlement date
    function getSettlementDate(uint256 assetType, uint256 maturity) public returns (uint256) {
        return
            AssetHandler.getSettlementDate(
                PortfolioAsset({
