// Original: contracts/7/contracts/mocks/helpers/MockReserveConfiguration.sol, lines 72-76
function setStableRateBorrowingEnabled(bool enabled) external {
    DataTypes.ReserveConfigurationMap memory config = configuration;
    config.setStableRateBorrowingEnabled(enabled);
    configuration = config;
  }

// Original: contracts/7/contracts/mocks/helpers/MockReserveConfiguration.sol, lines 78-80
function getStableRateBorrowingEnabled() external view returns (bool) {
    return configuration.getStableRateBorrowingEnabled();
  }

// Original: contracts/7/contracts/protocol/libraries/configuration/ReserveConfiguration.sol, lines 317-324
function setStableRateBorrowingEnabled(
    DataTypes.ReserveConfigurationMap memory self,
    bool enabled
  ) internal pure {
    self.data =
      (self.data & STABLE_BORROWING_MASK) |
      (uint256(enabled ? 1 : 0) << STABLE_BORROWING_ENABLED_START_BIT_POSITION);
  }

// Original: contracts/7/contracts/protocol/libraries/configuration/ReserveConfiguration.sol, lines 331-335
function getStableRateBorrowingEnabled(
    DataTypes.ReserveConfigurationMap memory self
  ) internal pure returns (bool) {
    return (self.data & ~STABLE_BORROWING_MASK) != 0;
  }
