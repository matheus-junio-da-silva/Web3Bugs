// Original: contracts/7/contracts/mocks/helpers/MockReserveConfiguration.sol, lines 1-25
// SPDX-License-Identifier: BUSL-1.1
pragma solidity ^0.8.0;

import {ReserveConfiguration} from '../../protocol/libraries/configuration/ReserveConfiguration.sol';
import {DataTypes} from '../../protocol/libraries/types/DataTypes.sol';

contract MockReserveConfiguration {
  using ReserveConfiguration for DataTypes.ReserveConfigurationMap;

  DataTypes.ReserveConfigurationMap public configuration;

  function setLtv(uint256 ltv) external {
    DataTypes.ReserveConfigurationMap memory config = configuration;
    config.setLtv(ltv);
    configuration = config;
  }

  function getLtv() external view returns (uint256) {
    return configuration.getLtv();
  }

  function setLiquidationBonus(uint256 bonus) external {
    DataTypes.ReserveConfigurationMap memory config = configuration;
    config.setLiquidationBonus(bonus);
    configuration = config;

// Original: contracts/7/contracts/protocol/libraries/configuration/ReserveConfiguration.sol, lines 212-216
  function setPaused(DataTypes.ReserveConfigurationMap memory self, bool paused) internal pure {
    self.data =
      (self.data & PAUSED_MASK) |
      (uint256(paused ? 1 : 0) << IS_PAUSED_START_BIT_POSITION);
  }

// Original: contracts/7/contracts/protocol/libraries/configuration/ReserveConfiguration.sol, lines 223-225
  function getPaused(DataTypes.ReserveConfigurationMap memory self) internal pure returns (bool) {
    return (self.data & ~PAUSED_MASK) != 0;
  }

