// Source: contracts/13/contracts/mocks/certora/LiquidityCurveHarness.sol
// Original lines: 1-35
// SPDX-License-Identifier: GPL-3.0-only
pragma solidity >0.7.0;
pragma experimental ABIEncoderV2;

import "../../internal/markets/CashGroup.sol";
import "../../internal/markets/Market.sol";
// import "../../math/ABDKMath64x64.sol";

contract LiquidityCurveHarness {
    using CashGroup for CashGroupParameters;
    using Market for MarketParameters;

    // using Market for mapping(uint256=>mapping(uint256=>mapping(uint256 => MarketParameters)));

    // mapping(uint256=>mapping(uint256=>mapping(uint256 => MarketParameters))) public symbolicMarkets;

    CashGroupParameters symbolicCashGroupStorage;

    MarketParameters symbolicMarket;

    uint256 private constant MARKET_INDEX = 1;
    uint256 private constant CURRENCY_ID = 1;
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