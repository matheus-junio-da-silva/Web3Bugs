// Original Solidity: contracts/15/facilitators/aave/interestStrategy/GhoDiscountRateStrategy.sol lines 25-25; storage
  uint256 public constant DISCOUNT_RATE = 0.3e4;

// Original Solidity: contracts/15/facilitators/aave/interestStrategy/GhoDiscountRateStrategy.sol lines 40-54; calculateDiscountRate
  function calculateDiscountRate(
    uint256 debtBalance,
    uint256 discountTokenBalance
  ) external pure override returns (uint256) {
    if (discountTokenBalance < MIN_DISCOUNT_TOKEN_BALANCE || debtBalance < MIN_DEBT_TOKEN_BALANCE) {
      return 0;
    } else {
      uint256 discountedBalance = discountTokenBalance.wadMul(GHO_DISCOUNTED_PER_DISCOUNT_TOKEN);
      if (discountedBalance >= debtBalance) {
        return DISCOUNT_RATE;
      } else {
        return (discountedBalance * DISCOUNT_RATE) / debtBalance;
      }
    }
  }
