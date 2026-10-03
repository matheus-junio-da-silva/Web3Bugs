// Extracted from: contracts/1/contracts/bridges/BridgeExecutorBase.sol
// Original source range: 35-41

  /**
   * @dev Only guardian can call functions marked by this modifier.
   **/
  modifier onlyGuardian() {
    if (msg.sender != _guardian) revert NotGuardian();
    _;
  }

// Extracted from: contracts/1/contracts/bridges/BridgeExecutorBase.sol
// Original source range: 82-132

  function execute(uint256 actionsSetId) external payable override {
    if (getCurrentState(actionsSetId) != ActionsSetState.Queued) revert OnlyQueuedActions();

    ActionsSet storage actionsSet = _actionsSets[actionsSetId];
    if (block.timestamp < actionsSet.executionTime) revert TimelockNotFinished();

    actionsSet.executed = true;
    uint256 actionCount = actionsSet.targets.length;

    bytes[] memory returnedData = new bytes[](actionCount);
    for (uint256 i = 0; i < actionCount; ) {
      returnedData[i] = _executeTransaction(
        actionsSet.targets[i],
        actionsSet.values[i],
        actionsSet.signatures[i],
        actionsSet.calldatas[i],
        actionsSet.executionTime,
        actionsSet.withDelegatecalls[i]
      );
      unchecked {
        ++i;
      }
    }

    emit ActionsSetExecuted(actionsSetId, msg.sender, returnedData);
  }

  /// @inheritdoc IExecutorBase
  function cancel(uint256 actionsSetId) external override onlyGuardian {
    if (getCurrentState(actionsSetId) != ActionsSetState.Queued) revert OnlyQueuedActions();

    ActionsSet storage actionsSet = _actionsSets[actionsSetId];
    actionsSet.canceled = true;

    uint256 targetsLength = actionsSet.targets.length;
    for (uint256 i = 0; i < targetsLength; ) {
      _cancelTransaction(
        actionsSet.targets[i],
        actionsSet.values[i],
        actionsSet.signatures[i],
        actionsSet.calldatas[i],
        actionsSet.executionTime,
        actionsSet.withDelegatecalls[i]
      );
      unchecked {
        ++i;
      }
    }

    emit ActionsSetCanceled(actionsSetId);
  }

// Extracted from: contracts/1/contracts/bridges/BridgeExecutorBase.sol
// Original source range: 223-241

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
