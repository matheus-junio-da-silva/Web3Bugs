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
// Original lines: 45-77
    }

    function getRateOracleTimeWindow() external returns (uint256) {
        symbolicCashGroupStorage._buildCashGroupView(CURRENCY_ID);
        // CashGroupParameters memory cashGroup = CashGroup.buildCashGroupView(CURRENCY_ID);
        // CashGroupParameters memory cashGroup = symbolicCashGroup;
        // return cashGroup.getRateOracleTimeWindow();
        // return symbolicCashGroup.getRateOracleTimeWindow();
        return symbolicCashGroupStorage.getRateOracleTimeWindowStorage();
    }

    function getStoredOracleRate() external view returns (uint256) {
        uint256 settlementDate = DateTime.getReferenceTime(block.timestamp) + Constants.QUARTER;
        bytes32 marketSlot = Market.getMarketSlot(CURRENCY_ID, settlementDate, MATURITY);
        return Market.oracleRateStorage(marketSlot);
        
        // Instead we could write:
        // return symbolicMarkets[CURRENCY_ID][settlementDate][MATURITY].oracleRateStorage;


        // bytes32 slot = Market.getSlot(CURRENCY_ID, settlementDate, MATURITY);
        // bytes32 data;

        // assembly {
        //     data := sload(slot)
        // }

        // uint256 oracleRate = uint256(uint32(uint256(data >> 192)));

        // return oracleRate;
    }

    function getLastImpliedRate() external returns (uint256) {
// Source: contracts/13/contracts/mocks/certora/LiquidityCurveHarness.sol
// Original lines: 90-122
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

// Source: contracts/13/contracts/mocks/certora/LiquidityCurveHarness.sol
// Original lines: 83-115
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

    function getMarketAssetCash() external returns (int256) {
        // uint256 settlementDate = _loadMarket();
         _loadMarket();
        // return symbolicMarkets[CURRENCY_ID][settlementDate][MATURITY].totalAssetCash;
        // return _loadMarket().totalAssetCash;
        return symbolicMarket.totalAssetCash;
    }
