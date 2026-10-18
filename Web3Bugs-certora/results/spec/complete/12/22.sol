// Original: contracts/12/specs/harness/UserConfigurationHarness.sol:13-14
  DataTypes.UserConfigurationMap internal usersConfig;


// Original: contracts/12/specs/harness/UserConfigurationHarness.sol:23-33
  function isUsingAsCollateralOrBorrowing(uint256 reserveIndex) public view returns (bool) {
    return UserConfiguration.isUsingAsCollateralOrBorrowing(usersConfig, reserveIndex);
  }

  function isBorrowing(uint256 reserveIndex) public view returns (bool) {
    return UserConfiguration.isBorrowing(usersConfig, reserveIndex);
  }

  function isUsingAsCollateral(uint256 reserveIndex) public view returns (bool) {
    return UserConfiguration.isUsingAsCollateral(usersConfig, reserveIndex);
  }

// Original: contracts/12/contracts/protocol/libraries/configuration/UserConfiguration.sol:56-62
  function isUsingAsCollateralOrBorrowing(
    DataTypes.UserConfigurationMap memory self,
    uint256 reserveIndex
  ) internal pure returns (bool) {
    require(reserveIndex < 128, Errors.UL_INVALID_INDEX);
    return (self.data >> (reserveIndex * 2)) & 3 != 0;
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
