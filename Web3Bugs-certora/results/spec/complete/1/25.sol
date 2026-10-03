// Extracted from: contracts/1/contracts/bridges/BridgeExecutorBase.sol
// Original source range: 17-26

  // Time between queuing and execution
  uint256 private _delay;
  // Time after the execution time during which the actions set can be executed
  uint256 private _gracePeriod;
  // Minimum allowed delay
  uint256 private _minimumDelay;
  // Maximum allowed delay
  uint256 private _maximumDelay;
  // Address with the ability of canceling actions sets
  address private _guardian;

// Extracted from: contracts/1/contracts/bridges/BridgeExecutorBase.sol
// Original source range: 135-163

  function updateGuardian(address guardian) external override onlyThis {
    _updateGuardian(guardian);
  }

  /// @inheritdoc IExecutorBase
  function updateDelay(uint256 delay) external override onlyThis {
    _validateDelay(delay);
    _updateDelay(delay);
  }

  /// @inheritdoc IExecutorBase
  function updateGracePeriod(uint256 gracePeriod) external override onlyThis {
    if (gracePeriod < MINIMUM_GRACE_PERIOD) revert GracePeriodTooShort();
    _updateGracePeriod(gracePeriod);
  }

  /// @inheritdoc IExecutorBase
  function updateMinimumDelay(uint256 minimumDelay) external override onlyThis {
    if (minimumDelay >= _maximumDelay) revert MinimumDelayTooLong();
    _updateMinimumDelay(minimumDelay);
    _validateDelay(_delay);
  }

  /// @inheritdoc IExecutorBase
  function updateMaximumDelay(uint256 maximumDelay) external override onlyThis {
    if (maximumDelay <= _minimumDelay) revert MaximumDelayTooShort();
    _updateMaximumDelay(maximumDelay);
    _validateDelay(_delay);
  }

// Extracted from: contracts/1/contracts/bridges/BridgeExecutorBase.sol
// Original source range: 183-210

  /// @inheritdoc IExecutorBase
  function getDelay() external view override returns (uint256) {
    return _delay;
  }

  /// @inheritdoc IExecutorBase
  function getGracePeriod() external view override returns (uint256) {
    return _gracePeriod;
  }

  /// @inheritdoc IExecutorBase
  function getMinimumDelay() external view override returns (uint256) {
    return _minimumDelay;
  }

  /// @inheritdoc IExecutorBase
  function getMaximumDelay() external view override returns (uint256) {
    return _maximumDelay;
  }

  /// @inheritdoc IExecutorBase
  function getGuardian() external view override returns (address) {
    return _guardian;
  }

  /// @inheritdoc IExecutorBase
  function getActionsSetCount() external view override returns (uint256) {
    return _actionsSetCounter;

// Extracted from: contracts/1/contracts/bridges/BridgeExecutorBase.sol
// Original source range: 243-266

  function _updateGuardian(address guardian) internal {
    emit GuardianUpdate(_guardian, guardian);
    _guardian = guardian;
  }

  function _updateDelay(uint256 delay) internal {
    emit DelayUpdate(_delay, delay);
    _delay = delay;
  }

  function _updateGracePeriod(uint256 gracePeriod) internal {
    emit GracePeriodUpdate(_gracePeriod, gracePeriod);
    _gracePeriod = gracePeriod;
  }

  function _updateMinimumDelay(uint256 minimumDelay) internal {
    emit MinimumDelayUpdate(_minimumDelay, minimumDelay);
    _minimumDelay = minimumDelay;
  }

  function _updateMaximumDelay(uint256 maximumDelay) internal {
    emit MaximumDelayUpdate(_maximumDelay, maximumDelay);
    _maximumDelay = maximumDelay;
  }

// Extracted from: contracts/1/contracts/bridges/BridgeExecutorBase.sol
// Original source range: 383-386

  function _validateDelay(uint256 delay) internal view {
    if (delay < _minimumDelay) revert DelayShorterThanMin();
    if (delay > _maximumDelay) revert DelayLongerThanMax();
  }
