// Original: contracts/9/contracts/governance/LockedGold.sol:139-168 (initialize)
  function initialize(address registryAddress, uint256 _unlockingPeriod) external initializer {
    _transferOwnership(msg.sender);
    setRegistry(registryAddress);
    setUnlockingPeriod(_unlockingPeriod);
    maxDelegateesCount = 10;
  }

  /**
   * @notice Sets the duration in seconds users must wait before withdrawing gold after unlocking.
   * @param value The unlocking period in seconds.
   */
  function setUnlockingPeriod(uint256 value) public onlyOwner {
    require(value != unlockingPeriod, "Unlocking period not changed");
    unlockingPeriod = value;
    emit UnlockingPeriodSet(value);
  }

  /**
   * @notice Sets max delegatees count.
   * @param value The max delegatees count.
   */
  function setMaxDelegateesCount(uint256 value) public onlyOwner {
    maxDelegateesCount = value;
    emit MaxDelegateesCountSet(value);
  }

  /**
   * @notice Locks gold to be used for voting.
   */
  function lock() external payable nonReentrant {

// Original: contracts/9/contracts/common/GoldToken.sol:64-93 (initialize)
  function initialize(address registryAddress) external initializer {
    totalSupply_ = 0;
    _transferOwnership(msg.sender);
    setRegistry(registryAddress);
  }

  /**
   * @notice Transfers CELO from one address to another.
   * @param to The address to transfer CELO to.
   * @param value The amount of CELO to transfer.
   * @return True if the transaction succeeds.
   */
  // solhint-disable-next-line no-simple-event-func-name
  function transfer(address to, uint256 value) external returns (bool) {
    return _transferWithCheck(to, value);
  }

  /**
   * @notice Transfers CELO from one address to another with a comment.
   * @param to The address to transfer CELO to.
   * @param value The amount of CELO to transfer.
   * @param comment The transfer comment
   * @return True if the transaction succeeds.
   */
  function transferWithComment(address to, uint256 value, string calldata comment)
    external
    returns (bool)
  {
    bool succeeded = _transferWithCheck(to, value);
    emit TransferComment(comment);

// Original: contracts/9/contracts/governance/Governance.sol:250-279 (initialize)
  function initialize(
    address registryAddress,
    address _approver,
    uint256 _concurrentProposals,
    uint256 _minDeposit,
    uint256 _queueExpiry,
    uint256 _dequeueFrequency,
    uint256 referendumStageDuration,
    uint256 executionStageDuration,
    uint256 participationBaseline,
    uint256 participationFloor,
    uint256 baselineUpdateFactor,
    uint256 baselineQuorumFactor
  ) external initializer {
    _transferOwnership(msg.sender);
    setRegistry(registryAddress);
    setApprover(_approver);
    setConcurrentProposals(_concurrentProposals);
    setMinDeposit(_minDeposit);
    setQueueExpiry(_queueExpiry);
    setDequeueFrequency(_dequeueFrequency);
    setReferendumStageDuration(referendumStageDuration);
    setExecutionStageDuration(executionStageDuration);
    setParticipationBaseline(participationBaseline);
    setParticipationFloor(participationFloor);
    setBaselineUpdateFactor(baselineUpdateFactor);
    setBaselineQuorumFactor(baselineQuorumFactor);
    // solhint-disable-next-line not-rely-on-time
    lastDequeue = now;
  }

// Original: contracts/9/contracts/common/Accounts.sol:139-168 (initialize)
  function initialize(address registryAddress) external initializer {
    _transferOwnership(msg.sender);
    setRegistry(registryAddress);
    setEip712DomainSeparator();
  }

  /**
   * @notice Sets the EIP712 domain separator for the Celo Accounts abstraction.
   */
  function setEip712DomainSeparator() public {
    uint256 chainId;
    assembly {
      chainId := chainid
    }

    eip712DomainSeparator = keccak256(
      abi.encode(
        keccak256(
          "EIP712Domain(string name,string version,uint256 chainId,address verifyingContract)"
        ),
        keccak256(bytes("Celo Core Contracts")),
        keccak256("1.0"),
        chainId,
        address(this)
      )
    );
  }

  /**
   * @notice Convenience Setter for the dataEncryptionKey and wallet address for an account
