// Source: contracts/13/contracts/mocks/certora/AccountPortfolioHarness.sol
// Original lines: 1-35
// SPDX-License-Identifier: GPL-3.0-only
pragma solidity >0.7.0;
pragma experimental ABIEncoderV2;

import "../../internal/AccountContextHandler.sol";
import "../../internal/balances/BalanceHandler.sol";
import "../../internal/portfolio/BitmapAssetsHandler.sol";
import "../../internal/portfolio/PortfolioHandler.sol";
import "../../internal/markets/DateTime.sol";

contract AccountPortfolioHarness {
    using AccountContextHandler for AccountContext;
    using PortfolioHandler for PortfolioState;
    using BalanceHandler for BalanceState;


    // todo : might need this as a mapping form address
    AccountContext public symbolicAccountContext;
    PortfolioState public symbolicPortfolioState;

    function getNextSettleTime(address account) external view returns (uint40) {
        //return AccountContextHandler.getAccountContext(account).nextSettleTime;
        return symbolicAccountContext.nextSettleTime;
    }

    function getHasDebt(address account) external view returns (uint8) {
        return uint8(symbolicAccountContext.hasDebt);
    }

    function getAssetArrayLength(address account) external view returns (uint8) {
        return symbolicAccountContext.assetArrayLength;
    }

    function getBitmapCurrency(address account) external view returns (uint16) {
        return symbolicAccountContext.bitmapCurrencyId;
