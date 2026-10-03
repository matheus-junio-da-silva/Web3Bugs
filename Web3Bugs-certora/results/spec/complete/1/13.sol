// Extracted from: contracts/1/contracts/interfaces/IExecutorBase.sol
// Original source range: 27-57

  /**
   * @notice This enum contains all possible actions set states
   */
  enum ActionsSetState {
    Queued,
    Executed,
    Canceled,
    Expired
  }

  /**
   * @notice This struct contains the data needed to execute a specified set of actions
   * @param targets Array of targets to call
   * @param values Array of values to pass in each call
   * @param signatures Array of function signatures to encode in each call (can be empty)
   * @param calldatas Array of calldatas to pass in each call, appended to the signature at the same array index if not empty
   * @param withDelegateCalls Array of whether to delegatecall for each call
   * @param executionTime Timestamp starting from which the actions set can be executed
   * @param executed True if the actions set has been executed, false otherwise
   * @param canceled True if the actions set has been canceled, false otherwise
   */
  struct ActionsSet {
    address[] targets;
    uint256[] values;
    string[] signatures;
    bytes[] calldatas;
    bool[] withDelegatecalls;
    uint256 executionTime;
    bool executed;
    bool canceled;
  }

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
// Original source range: 223-266

  /// @inheritdoc IExecutorBase
  function getCurrentState(uint256 actionsSetId) public view override returns (ActionsSetState) {
    if (_actionsSetCounter <= actionsSetId) revert InvalidActionsSetId();
    ActionsSet storage actionsSet = _actionsSets[actionsSetId];
    if (actionsSet.canceled) {
      return ActionsSetState.Canceled;
    } else if (actionsSet.executed) {
      return ActionsSetState.Executed;
    } else if (block.timestamp > actionsSet.executionTime + _gracePeriod) {
      return ActionsSetState.Expired;
    } else {
      return ActionsSetState.Queued;
    }
  }

  /// @inheritdoc IExecutorBase
  function isActionQueued(bytes32 actionHash) public view override returns (bool) {
    return _queuedActions[actionHash];
  }

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
