// Relevant excerpts for previewStakeEquivalentStake.
// Target Contract: StakedAaveV3Harness

// Source: contracts/4/contracts/StakedTokenV3.sol
// Original lines: 167-178;442-474

  function previewStake(uint256 assets) public view returns (uint256) {
    return (assets * _currentExchangeRate) / EXCHANGE_RATE_UNIT;
  }

  /// @inheritdoc IStakedTokenV2
  function stake(address to, uint256 amount)
    external
    override(IStakedTokenV2, StakedTokenV2)
  {
    _stake(msg.sender, to, amount);
  }

  function _stake(
    address from,
    address to,
    uint256 amount
  ) internal {
    require(!inPostSlashingPeriod, 'SLASHING_ONGOING');
    require(amount != 0, 'INVALID_ZERO_AMOUNT');

    uint256 balanceOfTo = balanceOf(to);

    uint256 accruedRewards = _updateUserAssetInternal(
      to,
      address(this),
      balanceOfTo,
      totalSupply()
    );

    if (accruedRewards != 0) {
      stakerRewardsToClaim[to] = stakerRewardsToClaim[to] + accruedRewards;
      emit RewardsAccrued(to, accruedRewards);
    }

    uint256 sharesToMint = previewStake(amount);

    STAKED_TOKEN.safeTransferFrom(from, address(this), amount);

    _mint(to, sharesToMint);

    emit Staked(from, to, amount, sharesToMint);
  }

  /**
   * @dev Redeems staked tokens, and stop earning rewards
