// Relevant excerpts for airdropNotMutualized.
// Target Contract: StakedAaveV3Harness

// Source: contracts/4/contracts/StakedTokenV3.sol
// Original lines: 45-50;256-258;532-536

  /// @notice The maximum amount of funds that can be slashed at any given time
  uint256 internal _maxSlashablePercentage;
  /// @notice Mirror of latest snapshot value for cheaper access
  uint216 internal _currentExchangeRate;
  /// @notice Flag determining if there's an ongoing slashing event that needs to be settled
  bool public inPostSlashingPeriod;
  function getExchangeRate() public view override returns (uint216) {
    return _currentExchangeRate;
  }
  function _updateExchangeRate(uint216 newExchangeRate) internal virtual {
    require(newExchangeRate != 0, 'ZERO_EXCHANGE_RATE');
    _currentExchangeRate = newExchangeRate;
    emit ExchangeRateChanged(newExchangeRate);
  }

// Source: contracts/4/certora/harness/DummyERC20Impl.sol
// Original lines: 53-61

  function transfer(address recipient, uint256 amount)
    external
    override
    returns (bool)
  {
    b[msg.sender] = sub(b[msg.sender], amount);
    b[recipient] = add(b[recipient], amount);
    return true;
  }
