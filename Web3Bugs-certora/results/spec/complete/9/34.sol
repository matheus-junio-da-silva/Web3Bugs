// Original: contracts/9/contracts/governance/Governance.sol:467-502 (function propose)
  function propose(
    uint256[] calldata values,
    address[] calldata destinations,
    bytes calldata data,
    uint256[] calldata dataLengths,
    string calldata descriptionUrl
  ) external payable returns (uint256) {
    dequeueProposalsIfReady();
    require(msg.value >= minDeposit, "Too small deposit");

    proposalCount = proposalCount.add(1);
    Proposals.Proposal storage proposal = proposals[proposalCount];
    proposal.make(values, destinations, data, dataLengths, msg.sender, msg.value);
    proposal.setDescriptionUrl(descriptionUrl);
    queue.push(proposalCount);
    // solhint-disable-next-line not-rely-on-time
    emit ProposalQueued(proposalCount, msg.sender, proposal.transactions.length, msg.value, now);
    return proposalCount;
  }

  /**
   * @notice Removes a proposal if it is queued and expired.
   * @param proposalId The ID of the proposal to remove.
   * @return Whether the proposal was removed.
   */
  function removeIfQueuedAndExpired(uint256 proposalId) private returns (bool) {
    if (isQueued(proposalId) && isQueuedProposalExpired(proposalId)) {
      queue.remove(proposalId);
      emit ProposalExpired(proposalId);
      return true;
    }
    return false;
  }

  /**
   * @notice Requires a proposal is dequeued and removes it if expired.
