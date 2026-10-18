// Source: contracts/13/contracts/mocks/certora/AccountPortfolioHarness.sol
// Original lines: 28-60
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
                    currencyId: 0,
                    maturity: maturity,
                    assetType: assetType,
                    notional: 0,

// Source: contracts/13/contracts/mocks/certora/AccountPortfolioHarness.sol
// Original lines: 103-135


    function getStoredAsset(address account, uint256 i) public view returns (uint256) {
        return symbolicPortfolioState.storedAssets[i].currencyId;
    }
    /** State Changing Methods **/

    function enableBitmapForAccount(
        address account,
        uint256 currencyId,
        uint256 blockTime
    ) external {
        AccountContext memory accountContext = symbolicAccountContext;
        accountContext.enableBitmapForAccount(account, currencyId, blockTime);
        symbolicAccountContext = accountContext;
    }

    // Adds one asset into the array portfolio at a time
    function addArrayAsset(
        address account,
        uint256 currencyId,
        uint256 maturity,
        uint256 assetType,
        int256 notional
    ) public {
        AccountContext memory accountContext = symbolicAccountContext;

        PortfolioState memory portfolioState = symbolicPortfolioState;
            
        portfolioState.addAsset(currencyId, maturity, assetType, notional, false);

        symbolicAccountContext = accountContext;
    }
