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



// Original: contracts/9/contracts/common/Initializable.sol:1-17 (inherited initialized state and initializer guard)
// SPDX-License-Identifier: LGPL-3.0-only
pragma solidity >=0.5.13 <0.9.0;

contract Initializable {
  bool public initialized;

  constructor(bool testingDeployment) public {
    if (!testingDeployment) {
      initialized = true;
    }
  }

  modifier initializer() {
    require(!initialized, "contract already initialized");
    initialized = true;
    _;
  }
}
