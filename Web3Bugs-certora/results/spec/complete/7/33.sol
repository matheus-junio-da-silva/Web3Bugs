// Original: contracts/7/contracts/protocol/tokenization/StableDebtToken.sol, lines 295-297
function principalBalanceOf(address user) external view virtual override returns (uint256) {
    return super.balanceOf(user);
  }

// Original: contracts/7/contracts/protocol/tokenization/StableDebtToken.sol, lines 101-112
function balanceOf(address account) public view virtual override returns (uint256) {
    uint256 accountBalance = super.balanceOf(account);
    uint256 stableRate = _userState[account].additionalData;
    if (accountBalance == 0) {
      return 0;
    }
    uint256 cumulatedInterest = MathUtils.calculateCompoundedInterest(
      stableRate,
      _timestamps[account]
    );
    return accountBalance.rayMul(cumulatedInterest);
  }

// Original: contracts/7/contracts/protocol/tokenization/StableDebtToken.sol, lines 254-270
function _calculateBalanceIncrease(
    address user
  ) internal view returns (uint256, uint256, uint256) {
    uint256 previousPrincipalBalance = super.balanceOf(user);

    if (previousPrincipalBalance == 0) {
      return (0, 0, 0);
    }

    uint256 newPrincipalBalance = balanceOf(user);

    return (
      previousPrincipalBalance,
      newPrincipalBalance,
      newPrincipalBalance - previousPrincipalBalance
    );
  }
