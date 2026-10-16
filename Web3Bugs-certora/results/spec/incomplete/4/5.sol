// Relevant excerpts for integrityOfReturnFunds.
// Target Contract: StakedAaveV3Harness

// Source: contracts/4/contracts/StakedTokenV3.sol
// Original lines: 256-268;299-308;545-552

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
  function _getExchangeRate(uint256 totalAssets, uint256 totalShares)
    internal
    pure
    returns (uint216)
  {
    return
      (((totalShares * EXCHANGE_RATE_UNIT) + totalAssets - 1) / totalAssets)
        .toUint216();

// Source: contracts/4/certora/harness/DummyERC20Impl.sol
// Original lines: 49-91

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

  function allowance(address owner, address spender)
    external
    view
    override
    returns (uint256)
  {
    return a[owner][spender];
  }

  function approve(address spender, uint256 amount)
    external
    override
    returns (bool)
  {
    a[msg.sender][spender] = amount;
    return true;
  }

  function transferFrom(
    address sender,
    address recipient,
    uint256 amount
  ) external override returns (bool) {
    b[sender] = sub(b[sender], amount);
    b[recipient] = add(b[recipient], amount);
    a[sender][msg.sender] = sub(a[sender][msg.sender], amount);
    return true;
  }
}
