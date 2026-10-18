// Original Solidity: contracts/15/facilitators/aave/tokens/GhoVariableDebtToken.sol lines 53-53; storage
  mapping(address => GhoUserState) internal _ghoUserState;

// Original Solidity: contracts/15/facilitators/aave/tokens/base/ScaledBalanceTokenBase.sol lines 37-39; scaledBalanceOf
  function scaledBalanceOf(address user) external view override returns (uint256) {
    return super.balanceOf(user);
  }

// Original Solidity: contracts/15/facilitators/aave/tokens/base/ScaledBalanceTokenBase.sol lines 49-51; scaledTotalSupply
  function scaledTotalSupply() public view virtual override returns (uint256) {
    return super.totalSupply();
  }
