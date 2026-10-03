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
// Original source range: 28-33

  // Number of actions sets
  uint256 private _actionsSetCounter;
  // Map of registered actions sets (id => ActionsSet)
  mapping(uint256 => ActionsSet) private _actionsSets;
  // Map of queued actions (actionHash => isQueued)
  mapping(bytes32 => bool) private _queuedActions;

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
