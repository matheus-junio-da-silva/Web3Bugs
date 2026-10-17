// Original: contracts/7/contracts/mocks/helpers/MockReserveConfiguration.sol, lines 52-56
function setFrozen(bool frozen) external {
    DataTypes.ReserveConfigurationMap memory config = configuration;
    config.setFrozen(frozen);
    configuration = config;
  }

// Original: contracts/7/contracts/mocks/helpers/MockReserveConfiguration.sol, lines 58-60
function getFrozen() external view returns (bool) {
    return configuration.getFrozen();
  }

// Original: contracts/7/contracts/protocol/libraries/configuration/ReserveConfiguration.sol, lines 192-196
function setFrozen(DataTypes.ReserveConfigurationMap memory self, bool frozen) internal pure {
    self.data =
      (self.data & FROZEN_MASK) |
      (uint256(frozen ? 1 : 0) << IS_FROZEN_START_BIT_POSITION);
  }

// Original: contracts/7/contracts/protocol/libraries/configuration/ReserveConfiguration.sol, lines 203-205
function getFrozen(DataTypes.ReserveConfigurationMap memory self) internal pure returns (bool) {
    return (self.data & ~FROZEN_MASK) != 0;
  }
