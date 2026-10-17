// Original: contracts/7/contracts/mocks/helpers/MockReserveConfiguration.sol, lines 132-136
function setLiquidationProtocolFee(uint256 liquidationProtocolFee) external {
    DataTypes.ReserveConfigurationMap memory config = configuration;
    config.setLiquidationProtocolFee(liquidationProtocolFee);
    configuration = config;
  }

// Original: contracts/7/contracts/mocks/helpers/MockReserveConfiguration.sol, lines 138-140
function getLiquidationProtocolFee() external view returns (uint256) {
    return configuration.getLiquidationProtocolFee();
  }

// Original: contracts/7/contracts/protocol/libraries/configuration/ReserveConfiguration.sol, lines 444-456
function setLiquidationProtocolFee(
    DataTypes.ReserveConfigurationMap memory self,
    uint256 liquidationProtocolFee
  ) internal pure {
    require(
      liquidationProtocolFee <= MAX_VALID_LIQUIDATION_PROTOCOL_FEE,
      Errors.INVALID_LIQUIDATION_PROTOCOL_FEE
    );

    self.data =
      (self.data & LIQUIDATION_PROTOCOL_FEE_MASK) |
      (liquidationProtocolFee << LIQUIDATION_PROTOCOL_FEE_START_BIT_POSITION);
  }

// Original: contracts/7/contracts/protocol/libraries/configuration/ReserveConfiguration.sol, lines 463-468
function getLiquidationProtocolFee(
    DataTypes.ReserveConfigurationMap memory self
  ) internal pure returns (uint256) {
    return
      (self.data & ~LIQUIDATION_PROTOCOL_FEE_MASK) >> LIQUIDATION_PROTOCOL_FEE_START_BIT_POSITION;
  }
