// Original Solidity: contracts/15/facilitators/aave/tokens/GhoVariableDebtToken.sol lines 258-314; updateDiscountDistribution
  function updateDiscountDistribution(
    address sender,
    address recipient,
    uint256 senderDiscountTokenBalance,
    uint256 recipientDiscountTokenBalance,
    uint256 amount
  ) external override onlyDiscountToken {
    uint256 senderPreviousScaledBalance = super.balanceOf(sender);
    uint256 recipientPreviousScaledBalance = super.balanceOf(recipient);

    uint256 index = POOL.getReserveNormalizedVariableDebt(_underlyingAsset);

    uint256 balanceIncrease;
    uint256 discountScaled;

    if (senderPreviousScaledBalance > 0) {
      (balanceIncrease, discountScaled) = _accrueDebtOnAction(
        sender,
        senderPreviousScaledBalance,
        _ghoUserState[sender].discountPercent,
        index
      );

      _burn(sender, discountScaled.toUint128());

      _refreshDiscountPercent(
        sender,
        super.balanceOf(sender).rayMul(index),
        senderDiscountTokenBalance - amount,
        _ghoUserState[sender].discountPercent
      );

      emit Transfer(address(0), sender, balanceIncrease);
      emit Mint(address(0), sender, balanceIncrease, balanceIncrease, index);
    }

    if (recipientPreviousScaledBalance > 0) {
      (balanceIncrease, discountScaled) = _accrueDebtOnAction(
        recipient,
        recipientPreviousScaledBalance,
        _ghoUserState[recipient].discountPercent,
        index
      );

      _burn(recipient, discountScaled.toUint128());

      _refreshDiscountPercent(
        recipient,
        super.balanceOf(recipient).rayMul(index),
        recipientDiscountTokenBalance + amount,
        _ghoUserState[recipient].discountPercent
      );

      emit Transfer(address(0), recipient, balanceIncrease);
      emit Mint(address(0), recipient, balanceIncrease, balanceIncrease, index);
    }
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

// Original Solidity: contracts/15/facilitators/aave/tokens/base/ScaledBalanceTokenBase.sol lines 37-39; scaledBalanceOf
  function scaledBalanceOf(address user) external view override returns (uint256) {
    return super.balanceOf(user);
  }
