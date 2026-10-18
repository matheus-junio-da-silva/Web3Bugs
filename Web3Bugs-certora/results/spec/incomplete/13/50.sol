// Project 13 example 50: original Solidity excerpt
// Source: contracts/13/contracts/mocks/certora/CashGroupHarness.sol
// Original lines: 5-43
import "../../internal/markets/CashGroup.sol";

contract CashGroupHarness {
    using CashGroup for CashGroupParameters;

    function getMaxMarketIndex(uint256 currencyId) public view returns (uint8) {
        return CashGroup.getMaxMarketIndex(currencyId);
    }

    function getRateScalar(
        uint256 currencyId,
        uint256 marketIndex,
        uint256 timeToMaturity
    ) public returns (int256 rateScalar) {
        CashGroupParameters memory cg = CashGroup.buildCashGroupStateful(currencyId);
        CashGroupParameters memory cgv = CashGroup.buildCashGroupView(currencyId);
        rateScalar = cg.getRateScalar(marketIndex, timeToMaturity);
        assert(cgv.getRateScalar(marketIndex, timeToMaturity) == rateScalar);
    }

    function getTotalFee(uint256 currencyId) public returns (uint256 fee) {
        CashGroupParameters memory cg = CashGroup.buildCashGroupStateful(currencyId);
        CashGroupParameters memory cgv = CashGroup.buildCashGroupView(currencyId);
        fee = cg.getTotalFee();
        assert(cgv.getTotalFee() == fee);
    }

    function getReserveFeeShare(uint256 currencyId) public returns (int256 share) {
        CashGroupParameters memory cg = CashGroup.buildCashGroupStateful(currencyId);
        CashGroupParameters memory cgv = CashGroup.buildCashGroupView(currencyId);
        share = cg.getReserveFeeShare();
        assert(cgv.getReserveFeeShare() == share);
        return share;
    }

    function getLiquidityHaircut(uint256 currencyId, uint256 assetType)
        public
        returns (uint256 haircut)
    {

// Source: contracts/13/contracts/internal/markets/CashGroup.sol
// Original lines: 277-309

    /// @notice Checks all cash group settings for invalid values and sets them into storage
    function setCashGroupStorage(uint256 currencyId, CashGroupSettings calldata cashGroup)
        internal
    {
        bytes32 slot = keccak256(abi.encode(currencyId, Constants.CASH_GROUP_STORAGE_OFFSET));
        require(
            cashGroup.maxMarketIndex >= 0 &&
                cashGroup.maxMarketIndex <= Constants.MAX_TRADED_MARKET_INDEX,
            "CG: invalid market index"
        );
        // Due to the requirements of the yield curve we do not allow a cash group to have solely a 3 month market.
        // The reason is that borrowers will not have a further maturity to roll from their 3 month fixed to a 6 month
        // fixed. It also complicates the logic in the nToken initialization method
        require(cashGroup.maxMarketIndex != 1, "CG: invalid market index");
        require(
            cashGroup.reserveFeeShare <= Constants.PERCENTAGE_DECIMALS,
            "CG: invalid reserve share"
        );
        require(cashGroup.liquidityTokenHaircuts.length == cashGroup.maxMarketIndex);
        require(cashGroup.rateScalars.length == cashGroup.maxMarketIndex);
        // This is required so that fCash liquidation can proceed correctly
        require(cashGroup.liquidationfCashHaircut5BPS < cashGroup.fCashHaircut5BPS);
        require(cashGroup.liquidationDebtBuffer5BPS < cashGroup.debtBuffer5BPS);

        // Market indexes cannot decrease or they will leave fCash assets stranded in the future with no valuation curve
        uint8 previousMaxMarketIndex = uint8(uint256(_getCashGroupStorageBytes(currencyId)));
        require(
            previousMaxMarketIndex <= cashGroup.maxMarketIndex,
            "CG: market index cannot decrease"
        );

        // Per cash group settings

// Source: contracts/13/contracts/internal/markets/CashGroup.sol
// Original lines: 109-141

    /// @notice Time window factor for the rate oracle denominated in seconds
    function getRateOracleTimeWindow(CashGroupParameters memory cashGroup)
        internal
        pure
        returns (uint256)
    {
        // This is denominated in minutes in storage
        return uint256(uint8(uint256(cashGroup.data >> RATE_ORACLE_TIME_WINDOW))) * 60;
    }

        function getRateOracleTimeWindowStorage(CashGroupParameters storage cashGroup)
        internal
        view
        returns (uint256)
    {
        // This is denominated in minutes in storage
        return uint256(uint8(uint256(cashGroup.data >> RATE_ORACLE_TIME_WINDOW))) * 60;
    }

    /// @notice Penalty rate for settling cash debts denominated in basis points
    function getSettlementPenalty(CashGroupParameters memory cashGroup)
        internal
        pure
        returns (uint256)
    {
        return
            uint256(uint8(uint256(cashGroup.data >> SETTLEMENT_PENALTY))) *
            (5 * Constants.BASIS_POINT);
    }

    /// @notice Haircut for fCash during liquidation denominated in basis points
    function getLiquidationfCashHaircut(CashGroupParameters memory cashGroup)
