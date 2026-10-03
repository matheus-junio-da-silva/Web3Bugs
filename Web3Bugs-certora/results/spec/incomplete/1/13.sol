// Extracted from: contracts/1/contracts/bridges/BridgeExecutorBase.sol
// Original source range: 17-33

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

  // Number of actions sets
  uint256 private _actionsSetCounter;
  // Map of registered actions sets (id => ActionsSet)
  mapping(uint256 => ActionsSet) private _actionsSets;
  // Map of queued actions (actionHash => isQueued)
  mapping(bytes32 => bool) private _queuedActions;

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
