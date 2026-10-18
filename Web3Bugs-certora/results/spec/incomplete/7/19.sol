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
