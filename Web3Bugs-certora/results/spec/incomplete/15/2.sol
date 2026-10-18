// Original Solidity: contracts/15/facilitators/aave/tokens/GhoVariableDebtToken.sol lines 145-155; mint
  function mint(
    address user,
    address onBehalfOf,
    uint256 amount,
    uint256 index
  ) external virtual override onlyPool returns (bool, uint256) {
    if (user != onBehalfOf) {
      _decreaseBorrowAllowance(onBehalfOf, user, amount);
    }
    return (_mintScaled(user, onBehalfOf, amount, index), scaledTotalSupply());
  }

// Original Solidity: contracts/15/facilitators/aave/tokens/GhoVariableDebtToken.sol lines 158-165; burn
  function burn(
    address from,
    uint256 amount,
    uint256 index
  ) external virtual override onlyPool returns (uint256) {
    _burnScaled(from, address(0), amount, index);
    return scaledTotalSupply();
  }

// Original Solidity: contracts/15/facilitators/aave/tokens/base/ScaledBalanceTokenBase.sol lines 37-39; scaledBalanceOf
  function scaledBalanceOf(address user) external view override returns (uint256) {
    return super.balanceOf(user);
  }

// Original Solidity: contracts/15/facilitators/aave/tokens/base/ScaledBalanceTokenBase.sol lines 49-51; scaledTotalSupply
  function scaledTotalSupply() public view virtual override returns (uint256) {
    return super.totalSupply();
  }
