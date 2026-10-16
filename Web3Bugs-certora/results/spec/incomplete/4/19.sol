// Relevant excerpts for integrityOfRedeem.
// Target Contract: StakedAaveV3Harness

// Source: contracts/4/contracts/StakedTokenV3.sol
// Original lines: 201-216;256-268;479-527

  function redeem(address to, uint256 amount)
    external
    override(IStakedTokenV2, StakedTokenV2)
  {
    _redeem(msg.sender, to, amount);
  }

  /// @inheritdoc IStakedTokenV3
  function redeemOnBehalf(
    address from,
    address to,
    uint256 amount
  ) external override onlyClaimHelper {
    _redeem(from, to, amount);
  }

  function getExchangeRate() public view override returns (uint216) {
    return _currentExchangeRate;
  }

  /// @inheritdoc IStakedTokenV3
  function previewRedeem(uint256 shares)
    public
    view
    override
    returns (uint256)
  {
    return (EXCHANGE_RATE_UNIT * shares) / _currentExchangeRate;
  }
  function _redeem(
    address from,
    address to,
    uint256 amount
  ) internal {
    require(amount != 0, 'INVALID_ZERO_AMOUNT');

    CooldownSnapshot memory cooldownSnapshot = stakersCooldowns[from];
    if (!inPostSlashingPeriod) {
      require(
        (block.timestamp >= cooldownSnapshot.timestamp + _cooldownSeconds),
        'INSUFFICIENT_COOLDOWN'
      );
      require(
        (block.timestamp - (cooldownSnapshot.timestamp + _cooldownSeconds) <=
          UNSTAKE_WINDOW),
        'UNSTAKE_WINDOW_FINISHED'
      );
    }

    uint256 balanceOfFrom = balanceOf(from);
    uint256 maxRedeemable = inPostSlashingPeriod
      ? balanceOfFrom
      : cooldownSnapshot.amount;
    require(maxRedeemable != 0, 'INVALID_ZERO_MAX_REDEEMABLE');

    uint256 amountToRedeem = (amount > maxRedeemable) ? maxRedeemable : amount;

    _updateCurrentUnclaimedRewards(from, balanceOfFrom, true);

    uint256 underlyingToRedeem = previewRedeem(amountToRedeem);

    _burn(from, amountToRedeem);

    if (cooldownSnapshot.timestamp != 0) {
      if (cooldownSnapshot.amount - amountToRedeem == 0) {
        delete stakersCooldowns[from];
      } else {
        stakersCooldowns[from].amount =
          stakersCooldowns[from].amount -
          amountToRedeem.toUint184();
      }
    }

    IERC20(STAKED_TOKEN).safeTransfer(to, underlyingToRedeem);

    emit Redeem(from, to, underlyingToRedeem, amountToRedeem);
  }


// Source: contracts/4/certora/harness/DummyERC20Impl.sol
// Original lines: 49-61

  function balanceOf(address account) public view override returns (uint256) {
    return b[account];
  }

  function transfer(address recipient, uint256 amount)
    external
    override
    returns (bool)
  {
    b[msg.sender] = sub(b[msg.sender], amount);
    b[recipient] = add(b[recipient], amount);
    return true;
  }

// Source: contracts/4/certora/harness/StakedAaveV3Harness.sol
// Original lines: 27-29

  function cooldownAmount(address user) public view returns (uint216) {
    return stakersCooldowns[user].amount;
  }
