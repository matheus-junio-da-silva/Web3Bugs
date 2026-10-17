// Original: contracts/7/contracts/mocks/helpers/MockReserveConfiguration.sol, lines 62-66
function setBorrowingEnabled(bool enabled) external {
    DataTypes.ReserveConfigurationMap memory config = configuration;
    config.setBorrowingEnabled(enabled);
    configuration = config;
  }

// Original: contracts/7/contracts/mocks/helpers/MockReserveConfiguration.sol, lines 68-70
function getBorrowingEnabled() external view returns (bool) {
    return configuration.getBorrowingEnabled();
  }

// Original: contracts/7/contracts/protocol/libraries/configuration/ReserveConfiguration.sol, lines 292-299
function setBorrowingEnabled(
    DataTypes.ReserveConfigurationMap memory self,
    bool enabled
  ) internal pure {
    self.data =
      (self.data & BORROWING_MASK) |
      (uint256(enabled ? 1 : 0) << BORROWING_ENABLED_START_BIT_POSITION);
  }

// Original: contracts/7/contracts/protocol/libraries/configuration/ReserveConfiguration.sol, lines 306-310
function getBorrowingEnabled(
    DataTypes.ReserveConfigurationMap memory self
  ) internal pure returns (bool) {
    return (self.data & ~BORROWING_MASK) != 0;
  }
