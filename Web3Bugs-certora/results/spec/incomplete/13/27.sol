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
// Original lines: 14-46
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

    function isValidMarketMaturity(
        uint256 maxMarketIndex,
        uint256 maturity,
        uint256 blockTime
    ) public pure returns (bool) {
        return DateTime.isValidMarketMaturity(maxMarketIndex, maturity, blockTime);
    }

// Source: contracts/13/contracts/internal/markets/DateTime.sol
// Original lines: 93-125
    /// of a given maturity.
    /// @return bitNum and a true or false if the maturity falls on the exact bit
    function getBitNumFromMaturity(uint256 blockTime, uint256 maturity)
        internal
        pure
        returns (uint256, bool)
    {
        uint256 blockTimeUTC0 = getTimeUTC0(blockTime);

        if (maturity % Constants.DAY != 0) return (0, false);
        if (blockTimeUTC0 >= maturity) return (0, false);

        // Overflow check done above
        uint256 daysOffset = (maturity - blockTimeUTC0) / Constants.DAY;

        // These if statements need to fall through to the next one
        if (daysOffset <= Constants.MAX_DAY_OFFSET) {
            return (daysOffset, true);
        }

        if (daysOffset <= Constants.MAX_WEEK_OFFSET) {
            uint256 offset =
                daysOffset -
                    Constants.MAX_DAY_OFFSET +
                    (blockTimeUTC0 % Constants.WEEK) /
                    Constants.DAY;
            // Ensures that the maturity specified falls on the actual day, otherwise division
            // will truncate it
            return (Constants.WEEK_BIT_OFFSET + offset / 6, (offset % 6) == 0);
        }

        if (daysOffset <= Constants.MAX_MONTH_OFFSET) {
            uint256 offset =
