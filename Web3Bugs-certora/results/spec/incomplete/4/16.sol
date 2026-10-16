// Relevant excerpts for returnFundsDecreaseExchangeRate.
// Target Contract: StakedAaveV3Harness

// Source: contracts/4/contracts/StakedTokenV3.sol
// Original lines: 34-50;256-268;299-308;532-552

  uint216 public constant INITIAL_EXCHANGE_RATE = 1e18;
  uint256 public constant EXCHANGE_RATE_UNIT = 1e18;

  /// @notice lower bound to prevent spam & avoid exchangeRate issues
  // as returnFunds can be called permissionless an attacker could spam returnFunds(1) to produce exchangeRate snapshots making voting expensive
  uint256 public immutable LOWER_BOUND;

  // Reserved storage space to allow for layout changes in the future.
  uint256[8] private ______gap;
  /// @notice Seconds between starting cooldown and being able to withdraw
  uint256 internal _cooldownSeconds;
  /// @notice The maximum amount of funds that can be slashed at any given time
  uint256 internal _maxSlashablePercentage;
  /// @notice Mirror of latest snapshot value for cheaper access
  uint216 internal _currentExchangeRate;
  /// @notice Flag determining if there's an ongoing slashing event that needs to be settled
  bool public inPostSlashingPeriod;
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
  function returnFunds(uint256 amount) external override {
    require(amount >= LOWER_BOUND, 'AMOUNT_LT_MINIMUM');
    uint256 currentShares = totalSupply();
    require(currentShares >= LOWER_BOUND, 'SHARES_LT_MINIMUM');
    uint256 assets = previewRedeem(currentShares);
    _updateExchangeRate(_getExchangeRate(assets + amount, currentShares));

    STAKED_TOKEN.safeTransferFrom(msg.sender, address(this), amount);
    emit FundsReturned(amount);
  }
  function _updateExchangeRate(uint216 newExchangeRate) internal virtual {
    require(newExchangeRate != 0, 'ZERO_EXCHANGE_RATE');
    _currentExchangeRate = newExchangeRate;
    emit ExchangeRateChanged(newExchangeRate);
  }

  /**
   * @dev calculates the exchange rate based on totalAssets and totalShares
   * @dev always rounds up to ensure 100% backing of shares by rounding in favor of the contract
   * @param totalAssets The total amount of assets staked
   * @param totalShares The total amount of shares
   * @return exchangeRate as 18 decimal precision uint216
   */
  function _getExchangeRate(uint256 totalAssets, uint256 totalShares)
    internal
    pure
    returns (uint216)
  {
    return
      (((totalShares * EXCHANGE_RATE_UNIT) + totalAssets - 1) / totalAssets)
        .toUint216();

// Source: contracts/4/contracts/StakedAaveV3.sol
// Original lines: 224-230

  function _updateExchangeRate(uint216 newExchangeRate) internal override {
    _exchangeRateSnapshots[_exchangeRateSnapshotsCount] = ExchangeRateSnapshot(
      block.number.toUint40(),
      newExchangeRate
    );
    ++_exchangeRateSnapshotsCount;
    super._updateExchangeRate(newExchangeRate);
