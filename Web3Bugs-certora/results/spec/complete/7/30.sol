// Original: contracts/7/contracts/mocks/helpers/MockReserveConfiguration.sol, lines 106-110
function setEModeCategory(uint256 categoryId) external {
    DataTypes.ReserveConfigurationMap memory config = configuration;
    config.setEModeCategory(categoryId);
    configuration = config;
  }

// Original: contracts/7/contracts/mocks/helpers/MockReserveConfiguration.sol, lines 102-104
function getEModeCategory() external view returns (uint256) {
    return configuration.getEModeCategory();
  }

// Original: contracts/7/contracts/protocol/libraries/configuration/ReserveConfiguration.sol, lines 502-509
function setEModeCategory(
    DataTypes.ReserveConfigurationMap memory self,
    uint256 category
  ) internal pure {
    require(category <= MAX_VALID_EMODE_CATEGORY, Errors.INVALID_EMODE_CATEGORY);

    self.data = (self.data & EMODE_CATEGORY_MASK) | (category << EMODE_CATEGORY_START_BIT_POSITION);
  }

// Original: contracts/7/contracts/protocol/libraries/configuration/ReserveConfiguration.sol, lines 516-520
function getEModeCategory(
    DataTypes.ReserveConfigurationMap memory self
  ) internal pure returns (uint256) {
    return (self.data & ~EMODE_CATEGORY_MASK) >> EMODE_CATEGORY_START_BIT_POSITION;
  }
