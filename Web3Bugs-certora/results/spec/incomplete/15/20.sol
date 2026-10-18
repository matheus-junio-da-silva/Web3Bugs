// Original Solidity: contracts/15/facilitators/aave/tokens/GhoVariableDebtToken.sol lines 121-142; balanceOf
  function balanceOf(address user) public view virtual override returns (uint256) {
    uint256 scaledBalance = super.balanceOf(user);

    if (scaledBalance == 0) {
      return 0;
    }

    uint256 index = POOL.getReserveNormalizedVariableDebt(_underlyingAsset);
    uint256 previousIndex = _userState[user].additionalData;
    uint256 balance = scaledBalance.rayMul(index);
    if (index == previousIndex) {
      return balance;
    }

    uint256 discountPercent = _ghoUserState[user].discountPercent;
    if (discountPercent != 0) {
      uint256 balanceIncrease = balance - scaledBalance.rayMul(previousIndex);
      balance -= balanceIncrease.percentMul(discountPercent);
    }

    return balance;
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
