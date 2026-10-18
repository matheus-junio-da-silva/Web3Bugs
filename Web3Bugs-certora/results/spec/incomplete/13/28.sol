// Source: contracts/13/contracts/mocks/certora/DateTimeHarness.sol
// Original lines: 6-38

contract DateTimeHarness {
    function getBitNumFromMaturity(uint256 blockTime, uint256 maturity)
        public
        pure
        returns (uint256, bool)
    {
        return DateTime.getBitNumFromMaturity(blockTime, maturity);
    }

    function getMaturityFromBitNum(uint256 blockTime, uint256 bitNum)
        public
        pure
        returns (uint256)
    {
        return DateTime.getMaturityFromBitNum(blockTime, bitNum);
    }

    function isValidMaturity(
        uint256 maxMarketIndex,
        uint256 maturity,
        uint256 blockTime
    ) public pure returns (bool) {
        return DateTime.isValidMaturity(maxMarketIndex, maturity, blockTime);
    }

    function getMarketIndex(
        uint256 maxMarketIndex,
        uint256 maturity,
        uint256 blockTime
    ) public pure returns (uint256, bool) {
        return DateTime.getMarketIndex(maxMarketIndex, maturity, blockTime);
    }

// Source: contracts/13/contracts/mocks/certora/DateTimeHarness.sol
// Original lines: 22-48
    }

    function isValidMaturity(
        uint256 maxMarketIndex,
        uint256 maturity,
        uint256 blockTime
    ) public pure returns (bool) {
        return DateTime.isValidMaturity(maxMarketIndex, maturity, blockTime);
    }

    function getMarketIndex(
        uint256 maxMarketIndex,
        uint256 maturity,
        uint256 blockTime
    ) public pure returns (uint256, bool) {
        return DateTime.getMarketIndex(maxMarketIndex, maturity, blockTime);
    }

    function isValidMarketMaturity(
        uint256 maxMarketIndex,
        uint256 maturity,
        uint256 blockTime
    ) public pure returns (bool) {
        return DateTime.isValidMarketMaturity(maxMarketIndex, maturity, blockTime);
    }
}


// Source: contracts/13/contracts/internal/markets/DateTime.sol
// Original lines: 57-89

    /// @notice Determines if an idiosyncratic maturity is valid and returns the bit reference that is the case.
    function isValidMaturity(
        uint256 maxMarketIndex,
        uint256 maturity,
        uint256 blockTime
    ) internal pure returns (bool) {
        uint256 tRef = DateTime.getReferenceTime(blockTime);
        uint256 maxMaturity = tRef.add(DateTime.getTradedMarket(maxMarketIndex));
        if (maturity > maxMaturity) return false;

        // prettier-ignore
        (/* */, bool isValid) = DateTime.getBitNumFromMaturity(blockTime, maturity);
        return isValid;
    }

    /// @notice Returns the market index for a given maturity
    function getMarketIndex(
        uint256 maxMarketIndex,
        uint256 maturity,
        uint256 blockTime
    ) internal pure returns (uint256, bool) {
        require(maxMarketIndex > 0, "CG: no markets listed");
        require(maxMarketIndex <= Constants.MAX_TRADED_MARKET_INDEX, "CG: market index bound");
        uint256 tRef = DateTime.getReferenceTime(blockTime);

        for (uint256 i = 1; i <= maxMarketIndex; i++) {
            uint256 marketMaturity = tRef.add(DateTime.getTradedMarket(i));
            if (marketMaturity == maturity) return (i, false);
            if (marketMaturity > maturity) return (i, true);
        }

        revert("CG: no market found");
