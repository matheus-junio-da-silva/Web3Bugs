// Original: contracts/12/specs/harness/UserConfigurationHarness.sol:13-17
  DataTypes.UserConfigurationMap internal usersConfig;

  function setBorrowing(uint256 reserveIndex, bool borrowing) public {
    UserConfiguration.setBorrowing(usersConfig, reserveIndex, borrowing);
  }

// Original: contracts/12/specs/harness/UserConfigurationHarness.sol:27-29
  function isBorrowing(uint256 reserveIndex) public view returns (bool) {
    return UserConfiguration.isBorrowing(usersConfig, reserveIndex);
  }

// Original: contracts/12/contracts/protocol/libraries/configuration/UserConfiguration.sol:22-31
  function setBorrowing(
    DataTypes.UserConfigurationMap storage self,
    uint256 reserveIndex,
    bool borrowing
  ) internal {
    require(reserveIndex < 128, Errors.UL_INVALID_INDEX);
    self.data =
      (self.data & ~(1 << (reserveIndex * 2))) |
      (uint256(borrowing ? 1 : 0) << (reserveIndex * 2));
  }

// Original: contracts/12/contracts/protocol/libraries/configuration/UserConfiguration.sol:70-77
  function isBorrowing(DataTypes.UserConfigurationMap memory self, uint256 reserveIndex)
    internal
    pure
    returns (bool)
  {
    require(reserveIndex < 128, Errors.UL_INVALID_INDEX);
    return (self.data >> (reserveIndex * 2)) & 1 != 0;
  }

// Original: contracts/12/contracts/protocol/libraries/types/DataTypes.sol:44-46
  struct UserConfigurationMap {
    uint256 data;
  }
