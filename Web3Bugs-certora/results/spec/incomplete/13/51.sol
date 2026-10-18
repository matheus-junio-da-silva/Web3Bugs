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

// Source: contracts/13/contracts/external/actions/GovernanceAction.sol
// Original lines: 116-148
    /// highest proportion of fCash where the nToken will provide liquidity. Above this proportion,
    /// the nToken will lend to the market instead to reduce the leverage in the market.
    function updateDepositParameters(
        uint16 currencyId,
        uint32[] calldata depositShares,
        uint32[] calldata leverageThresholds
    ) external override onlyOwner {
        require(
            depositShares.length == CashGroup.getMaxMarketIndex(currencyId),
            "Invalid array length"
        );
        nTokenHandler.setDepositParameters(currencyId, depositShares, leverageThresholds);
        emit UpdateDepositParameters(currencyId);
    }

    /// @notice Updates the market initialization parameters for an nToken
    /// @dev emit:UpdateInitializationParameters
    /// @param currencyId the currency id that the nToken references
    /// @param rateAnchors sets the offset from the x-axis where the liquidity curve will be
    /// initialized. This is used in combination with previous market rates to determine the
    /// initial proportion where markets will be initialized every quarter. Denominated in
    /// RATE_PRECISION as an exchange rate (i.e. must be > RATE_PRECISION)
    /// @param proportions used to combination with rateAnchors set the initial proportion when
    /// a market is first initialized. This is required since there is no previous rate to reference.
    function updateInitializationParameters(
        uint16 currencyId,
        uint32[] calldata rateAnchors,
        uint32[] calldata proportions
    ) external override onlyOwner {
        require(
            rateAnchors.length == CashGroup.getMaxMarketIndex(currencyId),
            "Invalid array length"
        );
