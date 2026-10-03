// Extracted from: contracts/1/contracts/bridges/BridgeExecutorBase.sol
// Original source range: 28-33

  // Number of actions sets
  uint256 private _actionsSetCounter;
  // Map of registered actions sets (id => ActionsSet)
  mapping(uint256 => ActionsSet) private _actionsSets;
  // Map of queued actions (actionHash => isQueued)
  mapping(bytes32 => bool) private _queuedActions;

// Extracted from: contracts/1/contracts/bridges/BridgeExecutorBase.sol
// Original source range: 82-107

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

// Extracted from: contracts/1/contracts/bridges/BridgeExecutorBase.sol
// Original source range: 239-241

  function isActionQueued(bytes32 actionHash) public view override returns (bool) {
    return _queuedActions[actionHash];
  }

// Extracted from: contracts/1/contracts/bridges/BridgeExecutorBase.sol
// Original source range: 336-381

  function _executeTransaction(
    address target,
    uint256 value,
    string memory signature,
    bytes memory data,
    uint256 executionTime,
    bool withDelegatecall
  ) internal returns (bytes memory) {
    if (address(this).balance < value) revert InsufficientBalance();

    bytes32 actionHash = keccak256(
      abi.encode(target, value, signature, data, executionTime, withDelegatecall)
    );
    _queuedActions[actionHash] = false;

    bytes memory callData;
    if (bytes(signature).length == 0) {
      callData = data;
    } else {
      callData = abi.encodePacked(bytes4(keccak256(bytes(signature))), data);
    }

    bool success;
    bytes memory resultData;
    if (withDelegatecall) {
      (success, resultData) = this.executeDelegateCall{value: value}(target, callData);
    } else {
      // solium-disable-next-line security/no-call-value
      (success, resultData) = target.call{value: value}(callData);
    }
    return _verifyCallResult(success, resultData);
  }

  function _cancelTransaction(
    address target,
    uint256 value,
    string memory signature,
    bytes memory data,
    uint256 executionTime,
    bool withDelegatecall
  ) internal {
    bytes32 actionHash = keccak256(
      abi.encode(target, value, signature, data, executionTime, withDelegatecall)
    );
    _queuedActions[actionHash] = false;
  }
