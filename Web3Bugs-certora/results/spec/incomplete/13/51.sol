// Project 13 example 51: original Solidity excerpt
// Source: contracts/13/contracts/mocks/certora/GovernanceActionHarness.sol
// Original lines: 41-79
    {
        ethRate = underlyingToETHRateMapping[currencyId];
        assetRate = assetToUnderlyingRateMapping[currencyId];
    }

    function getMaxMarketIndex(uint16 currencyId) external view returns (uint256) {
        return CashGroup.getMaxMarketIndex(currencyId);
    }

    /// @notice Returns market initialization parameters for a given currency
    function getInitializationParameters(uint16 currencyId)
        external
        view
        returns (int256[] memory rateAnchors, int256[] memory proportions)
    {
        uint256 maxMarketIndex = CashGroup.getMaxMarketIndex(currencyId);
        (rateAnchors, proportions) = nTokenHandler.getInitializationParameters(
            currencyId,
            maxMarketIndex
        );
    }

    /// @notice Returns nToken deposit parameters for a given currency
    function getDepositParameters(uint16 currencyId)
        external
        view
        returns (int256[] memory depositShares, int256[] memory leverageThresholds)
    {
        uint256 maxMarketIndex = CashGroup.getMaxMarketIndex(currencyId);
        (depositShares, leverageThresholds) = nTokenHandler.getDepositParameters(
            currencyId,
            maxMarketIndex
        );
    }

    /// @notice Returns nToken address for a given currency
    function nTokenAddress(uint16 currencyId) external view returns (address) {
        return nTokenHandler.nTokenAddress(currencyId);
    }
