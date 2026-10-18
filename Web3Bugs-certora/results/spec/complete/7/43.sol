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

// Original: contracts/7/contracts/protocol/tokenization/StableDebtToken.sol, lines 285-287
function totalSupply() public view virtual override returns (uint256) {
    return _calcTotalSupply(_avgStableRate);
  }
