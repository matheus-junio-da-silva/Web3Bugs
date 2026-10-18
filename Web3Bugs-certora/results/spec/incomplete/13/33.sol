// Source: contracts/13/contracts/mocks/certora/LiquidityCurveHarness.sol
// Original lines: 106-138
    }

    function getMarketAssetCash() external returns (int256) {
        // uint256 settlementDate = _loadMarket();
         _loadMarket();
        // return symbolicMarkets[CURRENCY_ID][settlementDate][MATURITY].totalAssetCash;
        // return _loadMarket().totalAssetCash;
        return symbolicMarket.totalAssetCash;
    }

    function getMarketLiquidity() external returns (int256) {
        // uint256 settlementDate = _loadMarket();
         _loadMarket();
        // return symbolicMarkets[CURRENCY_ID][settlementDate][MATURITY].totalLiquidity;
        // return _loadMarket().totalLiquidity;
        return symbolicMarket.totalLiquidity;
    }

    function executeTrade(uint256 timeToMaturity, int256 fCashToAccount)
        external
        returns (int256, int256)
    {
        // CashGroupParameters memory cashGroup = symbolicCashGroup; //CashGroup.buildCashGroupStateful(CURRENCY_ID);
        // CashGroupParameters memory cashGroup = CashGroup.buildCashGroupStateful(CURRENCY_ID);
        symbolicCashGroupStorage._buildCashGroupStateful(CURRENCY_ID);
        // MarketParameters memory market = symbolicMarket; //_loadMarket();
        //MarketParameters memory market = _loadMarket();
        //  uint256 settlementDate = _loadMarket();
         _loadMarket();
        //  MarketParameters storage market = symbolicMarkets[CURRENCY_ID][settlementDate][MATURITY];
        (int256 netAssetCash, int256 netAssetCashToReserve) =
            Market.calculateTrade(symbolicMarket, symbolicCashGroupStorage, fCashToAccount, timeToMaturity, MARKET_INDEX);
        // Market.setMarketStorage(market);

// Source: contracts/13/contracts/mocks/certora/LiquidityCurveHarness.sol
// Original lines: 122-154
    }

    function executeTrade(uint256 timeToMaturity, int256 fCashToAccount)
        external
        returns (int256, int256)
    {
        // CashGroupParameters memory cashGroup = symbolicCashGroup; //CashGroup.buildCashGroupStateful(CURRENCY_ID);
        // CashGroupParameters memory cashGroup = CashGroup.buildCashGroupStateful(CURRENCY_ID);
        symbolicCashGroupStorage._buildCashGroupStateful(CURRENCY_ID);
        // MarketParameters memory market = symbolicMarket; //_loadMarket();
        //MarketParameters memory market = _loadMarket();
        //  uint256 settlementDate = _loadMarket();
         _loadMarket();
        //  MarketParameters storage market = symbolicMarkets[CURRENCY_ID][settlementDate][MATURITY];
        (int256 netAssetCash, int256 netAssetCashToReserve) =
            Market.calculateTrade(symbolicMarket, symbolicCashGroupStorage, fCashToAccount, timeToMaturity, MARKET_INDEX);
        // Market.setMarketStorage(market);
        symbolicMarket.setMarketStorage();
        // symbolicMarket = market;
        // symbolicCashGroup = cashGroup;
        return (netAssetCash, netAssetCashToReserve);
    }

    function addLiquidity(int256 assetCash) external returns (int256, int256) {
        // MarketParameters memory market = symbolicMarket; //_loadMarket();
        // MarketParameters memory market = _loadMarket();
        //  uint256 settlementDate = _loadMarket();
         _loadMarket();
        //  MarketParameters storage market = symbolicMarkets[CURRENCY_ID][settlementDate][MATURITY];
        // int256 marketfCashBefore = market.totalfCash;
        (int256 liquidityTokens, int256 fCashToAccount) = symbolicMarket.addLiquidity( assetCash);
        // Market.setMarketStorage(market);
        symbolicMarket.setMarketStorage();
