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
// Original source range: 109-132

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
