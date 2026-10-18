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


// Original: contracts/9/contracts/governance/Governance.sol:353-388 (function setExecutionStageDuration)
  function setExecutionStageDuration(uint256 executionStageDuration) public onlyOwner {
    require(executionStageDuration != 0, "Duration must be larger than 0");
    require(executionStageDuration != stageDurations.execution, "Duration unchanged");
    stageDurations.execution = executionStageDuration;
    emit ExecutionStageDurationSet(executionStageDuration);
  }

  /**
   * @notice Updates the participation baseline.
   * @param participationBaseline The value of the baseline.
   */
  function setParticipationBaseline(uint256 participationBaseline) public onlyOwner {
    FixidityLib.Fraction memory participationBaselineFrac = FixidityLib.wrap(participationBaseline);
    require(
      FixidityLib.isProperFraction(participationBaselineFrac),
      "Participation baseline greater than one"
    );
    require(
      !participationBaselineFrac.equals(participationParameters.baseline),
      "Participation baseline unchanged"
    );
    participationParameters.baseline = participationBaselineFrac;
    emit ParticipationBaselineUpdated(participationBaseline);
  }

  /**
   * @notice Updates the floor of the participation baseline.
   * @param participationFloor The value at which the baseline is floored.
   */
  function setParticipationFloor(uint256 participationFloor) public onlyOwner {
    FixidityLib.Fraction memory participationFloorFrac = FixidityLib.wrap(participationFloor);
    require(
      FixidityLib.isProperFraction(participationFloorFrac),
      "Participation floor greater than one"
    );
    require(


// Original: contracts/9/contracts/governance/Governance.sol:342-377 (function setReferendumStageDuration)
  function setReferendumStageDuration(uint256 referendumStageDuration) public onlyOwner {
    require(referendumStageDuration != 0, "Duration must be larger than 0");
    require(referendumStageDuration != stageDurations.referendum, "Duration unchanged");
    stageDurations.referendum = referendumStageDuration;
    emit ReferendumStageDurationSet(referendumStageDuration);
  }

  /**
   * @notice Updates the number of seconds proposals stay in the execution stage.
   * @param executionStageDuration The number of seconds proposals stay in the execution stage.
   */
  function setExecutionStageDuration(uint256 executionStageDuration) public onlyOwner {
    require(executionStageDuration != 0, "Duration must be larger than 0");
    require(executionStageDuration != stageDurations.execution, "Duration unchanged");
    stageDurations.execution = executionStageDuration;
    emit ExecutionStageDurationSet(executionStageDuration);
  }

  /**
   * @notice Updates the participation baseline.
   * @param participationBaseline The value of the baseline.
   */
  function setParticipationBaseline(uint256 participationBaseline) public onlyOwner {
    FixidityLib.Fraction memory participationBaselineFrac = FixidityLib.wrap(participationBaseline);
    require(
      FixidityLib.isProperFraction(participationBaselineFrac),
      "Participation baseline greater than one"
    );
    require(
      !participationBaselineFrac.equals(participationParameters.baseline),
      "Participation baseline unchanged"
    );
    participationParameters.baseline = participationBaselineFrac;
    emit ParticipationBaselineUpdated(participationBaseline);
  }
