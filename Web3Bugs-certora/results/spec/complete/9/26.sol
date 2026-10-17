// Original: contracts/9/contracts/governance/Governance.sol:285-304 (function onlyOwner)
  function setApprover(address _approver) public onlyOwner {
    require(_approver != address(0), "Approver cannot be 0");
    require(_approver != approver, "Approver unchanged");
    approver = _approver;
    emit ApproverSet(_approver);
  }

  /**
   * @notice Updates the number of proposals to dequeue at a time.
   * @param _concurrentProposals The number of proposals to dequeue at at a time.
   */
  function setConcurrentProposals(uint256 _concurrentProposals) public onlyOwner {
    require(_concurrentProposals != 0, "Number of proposals must be larger than zero");
    require(_concurrentProposals != concurrentProposals, "Number of proposals unchanged");
    concurrentProposals = _concurrentProposals;
    emit ConcurrentProposalsSet(_concurrentProposals);
  }

  /**
   * @notice Updates the minimum deposit needed to make a proposal.
