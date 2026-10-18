// Original: contracts/12/specs/harness/UserConfigurationHarness.sol:13-14
  DataTypes.UserConfigurationMap internal usersConfig;


// Original: contracts/12/specs/harness/UserConfigurationHarness.sol:31-41
  function isUsingAsCollateral(uint256 reserveIndex) public view returns (bool) {
    return UserConfiguration.isUsingAsCollateral(usersConfig, reserveIndex);
  }

  function isBorrowingAny() public view returns (bool) {
    return UserConfiguration.isBorrowingAny(usersConfig);
  }

  function isEmpty() public view returns (bool) {
    return UserConfiguration.isEmpty(usersConfig);
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

// Original: contracts/12/contracts/protocol/libraries/configuration/UserConfiguration.sol:99-110
  function isBorrowingAny(DataTypes.UserConfigurationMap memory self) internal pure returns (bool) {
    return self.data & BORROWING_MASK != 0;
  }

  /**
   * @dev Used to validate if a user has not been using any reserve
   * @param self The configuration object
   * @return True if the user has been borrowing any reserve, false otherwise
   **/
  function isEmpty(DataTypes.UserConfigurationMap memory self) internal pure returns (bool) {
    return self.data == 0;
  }

// Original: contracts/12/contracts/protocol/libraries/types/DataTypes.sol:44-46
  struct UserConfigurationMap {
    uint256 data;
  }
