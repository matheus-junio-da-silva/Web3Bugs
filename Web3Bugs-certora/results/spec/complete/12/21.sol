// Original: contracts/12/specs/harness/UserConfigurationHarness.sol:13-14
  DataTypes.UserConfigurationMap internal usersConfig;


// Original: contracts/12/specs/harness/UserConfigurationHarness.sol:27-29
  function isBorrowing(uint256 reserveIndex) public view returns (bool) {
    return UserConfiguration.isBorrowing(usersConfig, reserveIndex);
  }

// Original: contracts/12/specs/harness/UserConfigurationHarness.sol:35-37
  function isBorrowingAny() public view returns (bool) {
    return UserConfiguration.isBorrowingAny(usersConfig);
  }

// Original: contracts/12/contracts/protocol/libraries/configuration/UserConfiguration.sol:12-15
library UserConfiguration {
  uint256 internal constant BORROWING_MASK =
    0x5555555555555555555555555555555555555555555555555555555555555555;


// Original: contracts/12/contracts/protocol/libraries/configuration/UserConfiguration.sol:70-77
  function isBorrowing(DataTypes.UserConfigurationMap memory self, uint256 reserveIndex)
    internal
    pure
    returns (bool)
  {
    require(reserveIndex < 128, Errors.UL_INVALID_INDEX);
    return (self.data >> (reserveIndex * 2)) & 1 != 0;
  }

// Original: contracts/12/contracts/protocol/libraries/configuration/UserConfiguration.sol:99-101
  function isBorrowingAny(DataTypes.UserConfigurationMap memory self) internal pure returns (bool) {
    return self.data & BORROWING_MASK != 0;
  }

// Original: contracts/12/contracts/protocol/libraries/types/DataTypes.sol:44-46
  struct UserConfigurationMap {
    uint256 data;
  }
