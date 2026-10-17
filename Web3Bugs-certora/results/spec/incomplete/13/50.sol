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
