// Extracted from: contracts/1/contracts/bridges/BridgeExecutorBase.sol
// Original source range: 17-20

  // Time between queuing and execution
  uint256 private _delay;
  // Time after the execution time during which the actions set can be executed
  uint256 private _gracePeriod;

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
// Original source range: 183-190

  /// @inheritdoc IExecutorBase
  function getDelay() external view override returns (uint256) {
    return _delay;
  }

  /// @inheritdoc IExecutorBase
  function getGracePeriod() external view override returns (uint256) {
    return _gracePeriod;

// Extracted from: contracts/1/contracts/bridges/BridgeExecutorBase.sol
// Original source range: 277-334

  function _queue(
    address[] memory targets,
    uint256[] memory values,
    string[] memory signatures,
    bytes[] memory calldatas,
    bool[] memory withDelegatecalls
  ) internal {
    if (targets.length == 0) revert EmptyTargets();
    uint256 targetsLength = targets.length;
    if (
      targetsLength != values.length ||
      targetsLength != signatures.length ||
      targetsLength != calldatas.length ||
      targetsLength != withDelegatecalls.length
    ) revert InconsistentParamsLength();

    uint256 actionsSetId = _actionsSetCounter;
    uint256 executionTime = block.timestamp + _delay;
    unchecked {
      ++_actionsSetCounter;
    }

    for (uint256 i = 0; i < targetsLength; ) {
      bytes32 actionHash = keccak256(
        abi.encode(
          targets[i],
          values[i],
          signatures[i],
          calldatas[i],
          executionTime,
          withDelegatecalls[i]
        )
      );
      if (isActionQueued(actionHash)) revert DuplicateAction();
      _queuedActions[actionHash] = true;
      unchecked {
        ++i;
      }
    }

    ActionsSet storage actionsSet = _actionsSets[actionsSetId];
    actionsSet.targets = targets;
    actionsSet.values = values;
    actionsSet.signatures = signatures;
    actionsSet.calldatas = calldatas;
    actionsSet.withDelegatecalls = withDelegatecalls;
    actionsSet.executionTime = executionTime;

    emit ActionsSetQueued(
      actionsSetId,
      targets,
      values,
      signatures,
      calldatas,
      withDelegatecalls,
      executionTime
    );
  }

// Extracted from: contracts/1/contracts/bridges/L2BridgeExecutor.sol
// Original source range: 18-21

  /**
   * @dev Only the Ethereum Governance Executor should be able to call functions marked by this modifier.
   **/
  modifier onlyEthereumGovernanceExecutor() virtual;

// Extracted from: contracts/1/contracts/bridges/L2BridgeExecutor.sol
// Original source range: 44-53

  /// @inheritdoc IL2BridgeExecutor
  function queue(
    address[] memory targets,
    uint256[] memory values,
    string[] memory signatures,
    bytes[] memory calldatas,
    bool[] memory withDelegatecalls
  ) external onlyEthereumGovernanceExecutor {
    _queue(targets, values, signatures, calldatas, withDelegatecalls);
  }

// Extracted from: contracts/1/contracts/bridges/OptimismBridgeExecutor.sol
// Original source range: 18-26

  /// @inheritdoc L2BridgeExecutor
  modifier onlyEthereumGovernanceExecutor() override {
    if (
      msg.sender != OVM_L2_CROSS_DOMAIN_MESSENGER ||
      ICrossDomainMessenger(OVM_L2_CROSS_DOMAIN_MESSENGER).xDomainMessageSender() !=
      _ethereumGovernanceExecutor
    ) revert UnauthorizedEthereumExecutor();
    _;
  }

// Extracted from: contracts/1/contracts/bridges/ArbitrumBridgeExecutor.sol
// Original source range: 14-19

  /// @inheritdoc L2BridgeExecutor
  modifier onlyEthereumGovernanceExecutor() override {
    if (AddressAliasHelper.undoL1ToL2Alias(msg.sender) != _ethereumGovernanceExecutor)
      revert UnauthorizedEthereumExecutor();
    _;
  }
