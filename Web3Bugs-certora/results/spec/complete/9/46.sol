// Original: contracts/9/contracts/governance/Governance.sol:250-285 (function initialize)
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

  /**
   * @notice Updates the address that has permission to approve proposals in the approval stage.
   * @param _approver The address that has permission to approve proposals in the approval stage.
   */
  function setApprover(address _approver) public onlyOwner {

// Original: contracts/9/contracts/common/Accounts.sol:139-174 (function initialize)
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
   * @param name A string to set as the name of the account
   * @param dataEncryptionKey secp256k1 public key for data encryption. Preferably compressed.
   * @param walletAddress The wallet address to set for the account
   * @param v The recovery id of the incoming ECDSA signature.
   * @param r Output value r of the ECDSA signature.
   * @param s Output value s of the ECDSA signature.
