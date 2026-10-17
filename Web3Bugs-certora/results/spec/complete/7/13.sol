// Original: contracts/7/contracts/mocks/helpers/MockReserveConfiguration.sol, lines 12-16
function setLtv(uint256 ltv) external {
    DataTypes.ReserveConfigurationMap memory config = configuration;
    config.setLtv(ltv);
    configuration = config;
  }

// Original: contracts/7/contracts/mocks/helpers/MockReserveConfiguration.sol, lines 18-20
function getLtv() external view returns (uint256) {
    return configuration.getLtv();
  }

// Original: contracts/7/contracts/protocol/libraries/configuration/ReserveConfiguration.sol, lines 73-77
function setLtv(DataTypes.ReserveConfigurationMap memory self, uint256 ltv) internal pure {
    require(ltv <= MAX_VALID_LTV, Errors.INVALID_LTV);

    self.data = (self.data & LTV_MASK) | ltv;
  }

// Original: contracts/7/contracts/protocol/libraries/configuration/ReserveConfiguration.sol, lines 84-86
function getLtv(DataTypes.ReserveConfigurationMap memory self) internal pure returns (uint256) {
    return self.data & ~LTV_MASK;
  }
