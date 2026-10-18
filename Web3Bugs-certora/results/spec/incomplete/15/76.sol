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

// Original Solidity: contracts/15/facilitators/aave/tokens/GhoVariableDebtToken.sol lines 333-356; rebalanceUserDiscountPercent
  function rebalanceUserDiscountPercent(address user) external override {
    uint256 index = POOL.getReserveNormalizedVariableDebt(_underlyingAsset);
    uint256 previousScaledBalance = super.balanceOf(user);
    uint256 discountPercent = _ghoUserState[user].discountPercent;

    (uint256 balanceIncrease, uint256 discountScaled) = _accrueDebtOnAction(
      user,
      previousScaledBalance,
      discountPercent,
      index
    );

    _burn(user, discountScaled.toUint128());

    _refreshDiscountPercent(
      user,
      super.balanceOf(user).rayMul(index),
      _discountToken.balanceOf(user),
      discountPercent
    );

    emit Transfer(address(0), user, balanceIncrease);
    emit Mint(address(0), user, balanceIncrease, balanceIncrease, index);
  }
