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

// Original: contracts/7/contracts/protocol/libraries/configuration/ReserveConfiguration.sol, lines 419-426
  function setDebtCeiling(
    DataTypes.ReserveConfigurationMap memory self,
    uint256 ceiling
  ) internal pure {
    require(ceiling <= MAX_VALID_DEBT_CEILING, Errors.INVALID_DEBT_CEILING);

    self.data = (self.data & DEBT_CEILING_MASK) | (ceiling << DEBT_CEILING_START_BIT_POSITION);
  }

// Original: contracts/7/contracts/protocol/libraries/configuration/ReserveConfiguration.sol, lines 433-437
  function getDebtCeiling(
    DataTypes.ReserveConfigurationMap memory self
  ) internal pure returns (uint256) {
    return (self.data & ~DEBT_CEILING_MASK) >> DEBT_CEILING_START_BIT_POSITION;
  }

