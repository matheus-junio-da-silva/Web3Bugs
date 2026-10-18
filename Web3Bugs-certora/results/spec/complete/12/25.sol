// Original: contracts/12/specs/harness/UserConfigurationHarness.sol:13-14
  DataTypes.UserConfigurationMap internal usersConfig;


// Original: contracts/12/specs/harness/UserConfigurationHarness.sol:19-21
  function setUsingAsCollateral(uint256 reserveIndex, bool _usingAsCollateral) public {
    UserConfiguration.setUsingAsCollateral(usersConfig, reserveIndex, _usingAsCollateral);
  }

// Original: contracts/12/specs/harness/UserConfigurationHarness.sol:31-33
  function isUsingAsCollateral(uint256 reserveIndex) public view returns (bool) {
    return UserConfiguration.isUsingAsCollateral(usersConfig, reserveIndex);
  }

// Original: contracts/12/contracts/protocol/libraries/configuration/UserConfiguration.sol:39-48
  function setUsingAsCollateral(
    DataTypes.UserConfigurationMap storage self,
    uint256 reserveIndex,
    bool usingAsCollateral
  ) internal {
    require(reserveIndex < 128, Errors.UL_INVALID_INDEX);
    self.data =
      (self.data & ~(1 << (reserveIndex * 2 + 1))) |
      (uint256(usingAsCollateral ? 1 : 0) << (reserveIndex * 2 + 1));
  }

// Original: contracts/12/contracts/protocol/libraries/configuration/UserConfiguration.sol:85-92
  function isUsingAsCollateral(DataTypes.UserConfigurationMap memory self, uint256 reserveIndex)
    internal
    pure
    returns (bool)
  {
    require(reserveIndex < 128, Errors.UL_INVALID_INDEX);
    return (self.data >> (reserveIndex * 2 + 1)) & 1 != 0;
  }

// Original: contracts/12/contracts/protocol/libraries/types/DataTypes.sol:44-46
  struct UserConfigurationMap {
    uint256 data;
  }
