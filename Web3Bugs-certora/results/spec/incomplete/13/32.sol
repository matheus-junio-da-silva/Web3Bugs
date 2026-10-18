// Source: contracts/13/contracts/mocks/certora/LiquidityCurveHarness.sol
// Original lines: 23-55
    uint256 public constant MATURITY = 86400 * 360 * 30;

   function getRateScalar(uint256 timeToMaturity) external returns (int256) {
        // CashGroupParameters memory cashGroup = CashGroup.buildCashGroupView(CURRENCY_ID);
        // CashGroupParameters memory cashGroup = symbolicCashGroup; //CashGroup.buildCashGroupView(CURRENCY_ID);
        // return symbolicCashGroup.getRateScalar(MARKET_INDEX, timeToMaturity);
        symbolicCashGroupStorage._buildCashGroupView(CURRENCY_ID);
        return symbolicCashGroupStorage.getRateScalarStorage(MARKET_INDEX, timeToMaturity);
    }

    function _loadMarket() internal returns(uint256 settlementDate) { // CERTORA: now returning the settlementDate // returns (MarketParameters memory) {
         symbolicCashGroupStorage._buildCashGroupView(CURRENCY_ID);
        // CashGroupParameters memory cashGroup = CashGroup.buildCashGroupView(CURRENCY_ID);
        // MarketParameters memory market;
        settlementDate = symbolicMarket.loadMarket(
            CURRENCY_ID,
            MATURITY,
            block.timestamp,
            true,
            symbolicCashGroupStorage.getRateOracleTimeWindowStorage()
        );
       // return market;
    }

    function getRateOracleTimeWindow() external returns (uint256) {
        symbolicCashGroupStorage._buildCashGroupView(CURRENCY_ID);
        // CashGroupParameters memory cashGroup = CashGroup.buildCashGroupView(CURRENCY_ID);
        // CashGroupParameters memory cashGroup = symbolicCashGroup;
        // return cashGroup.getRateOracleTimeWindow();
        // return symbolicCashGroup.getRateOracleTimeWindow();
        return symbolicCashGroupStorage.getRateOracleTimeWindowStorage();
    }


// Source: contracts/13/contracts/mocks/certora/LiquidityCurveHarness.sol
// Original lines: 75-107
    }

    function getLastImpliedRate() external returns (uint256) {
        // uint256 settlementDate = _loadMarket();
         _loadMarket();
        // return symbolicMarkets[CURRENCY_ID][settlementDate][MATURITY].lastImpliedRate;
        // return _loadMarket().lastImpliedRate;
        return symbolicMarket.lastImpliedRate;
    }

    function getPreviousTradeTime() external returns (uint256) {
        // uint256 settlementDate = _loadMarket();
         _loadMarket();
        // return symbolicMarkets[CURRENCY_ID][settlementDate][MATURITY].previousTradeTime;
        return symbolicMarket.previousTradeTime;
    }

    function getMarketOracleRate() external returns (uint256) {
        // uint256 settlementDate = _loadMarket();
         _loadMarket();
        // return symbolicMarkets[CURRENCY_ID][settlementDate][MATURITY].oracleRate;
        // return _loadMarket().oracleRate;
        return symbolicMarket.oracleRate;
    }

    function getMarketfCash() external returns (int256) {
        // uint256 settlementDate = _loadMarket();
         _loadMarket();
        // return symbolicMarkets[CURRENCY_ID][settlementDate][MATURITY].totalfCash;
        // return _loadMarket().totalfCash;
        return symbolicMarket.totalfCash;
    }
