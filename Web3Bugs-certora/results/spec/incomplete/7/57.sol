// Original: contracts/7/contracts/protocol/libraries/configuration/UserConfiguration.sol, lines 162-164
function isEmpty(DataTypes.UserConfigurationMap memory self) internal pure returns (bool) {
    return self.data == 0;
  }

// Original: contracts/7/contracts/protocol/libraries/configuration/UserConfiguration.sol, lines 153-155
function isBorrowingAny(DataTypes.UserConfigurationMap memory self) internal pure returns (bool) {
    return self.data & BORROWING_MASK != 0;
  }

// Original: contracts/7/contracts/protocol/libraries/configuration/UserConfiguration.sol, lines 71-79
function isUsingAsCollateralOrBorrowing(
    DataTypes.UserConfigurationMap memory self,
    uint256 reserveIndex
  ) internal pure returns (bool) {
    unchecked {
      require(reserveIndex < ReserveConfiguration.MAX_RESERVES_COUNT, Errors.INVALID_RESERVE_INDEX);
      return (self.data >> (reserveIndex << 1)) & 3 != 0;
    }
  }
