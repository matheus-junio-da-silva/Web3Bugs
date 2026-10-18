// Original: contracts/7/contracts/protocol/libraries/configuration/ReserveConfiguration.sol, lines 172-176
function setActive(DataTypes.ReserveConfigurationMap memory self, bool active) internal pure {
    self.data =
      (self.data & ACTIVE_MASK) |
      (uint256(active ? 1 : 0) << IS_ACTIVE_START_BIT_POSITION);
  }

// Original: contracts/7/contracts/protocol/libraries/configuration/ReserveConfiguration.sol, lines 183-185
function getActive(DataTypes.ReserveConfigurationMap memory self) internal pure returns (bool) {
    return (self.data & ~ACTIVE_MASK) != 0;
  }
