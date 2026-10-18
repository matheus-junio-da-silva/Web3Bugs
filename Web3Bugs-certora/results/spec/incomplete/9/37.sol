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

// Original: contracts/9/contracts/governance/Governance.sol:1102-1137 (function getVoteRecord)
  function getVoteRecord(address account, uint256 index)
    external
    view
    returns (uint256, uint256, uint256, uint256, uint256, uint256)
  {
    VoteRecord storage record = voters[account].referendumVotes[index];
    return (
      record.proposalId,
      uint256(record.deprecated_value),
      record.deprecated_weight,
      record.yesVotes,
      record.noVotes,
      record.abstainVotes
    );
  }

  /**
   * @notice Returns the number of proposals in the queue.
   * @return The number of proposals in the queue.
   */
  function getQueueLength() external view returns (uint256) {
    return queue.list.numElements;
  }

  /**
   * @notice Returns the number of upvotes the queued proposal has received.
   * @param proposalId The ID of the proposal.
   * @return The number of upvotes a queued proposal has received.
   */
  function getUpvotes(uint256 proposalId) external view returns (uint256) {
    require(isQueued(proposalId), "Proposal not queued");
    return queue.getValue(proposalId);
  }

  /**
   * @notice Returns the proposal ID and upvote total for all queued proposals.

// Original: contracts/9/contracts/governance/Governance.sol:1087-1122 (function getVoteTotals)
  function getVoteTotals(uint256 proposalId) external view returns (uint256, uint256, uint256) {
    return proposals[proposalId].getVoteTotals();
  }

  /**
   * @notice Returns an accounts vote record on a particular index in `dequeued`.
   * @param account The address of the account to get the record for.
   * @param index The index in `dequeued`.
   * @return The corresponding proposal ID, vote value, and weight.
   * @return The depreciated vote value.
   * @return The deprecieated weight.
   * @return The yes weight.
   * @return The no weight.
   * @return The abstain weight.
   */
  function getVoteRecord(address account, uint256 index)
    external
    view
    returns (uint256, uint256, uint256, uint256, uint256, uint256)
  {
    VoteRecord storage record = voters[account].referendumVotes[index];
    return (
      record.proposalId,
      uint256(record.deprecated_value),
      record.deprecated_weight,
      record.yesVotes,
      record.noVotes,
      record.abstainVotes
    );
  }

  /**
   * @notice Returns the number of proposals in the queue.
   * @return The number of proposals in the queue.
   */
  function getQueueLength() external view returns (uint256) {

// Original: contracts/9/contracts/governance/Governance.sol:644-679 (function vote)
  function vote(uint256 proposalId, uint256 index, Proposals.VoteValue value)
    external
    nonReentrant
    returns (bool)
  {
    dequeueProposalsIfReady();
    (Proposals.Proposal storage proposal, Proposals.Stage stage) = requireDequeuedAndDeleteExpired(
      proposalId,
      index
    );
    if (!proposal.exists()) {
      return false;
    }

    require(stage == Proposals.Stage.Referendum, "Incorrect proposal state");
    require(value != Proposals.VoteValue.None, "Vote value unset");

    address account = getAccounts().voteSignerToAccount(msg.sender);
    uint256 weight = getLockedGold().getAccountTotalGovernanceVotingPower(account);
    require(weight != 0, "Voter weight zero");

    _vote(
      proposal,
      proposalId,
      index,
      account,
      value == Proposals.VoteValue.Yes ? weight : 0,
      value == Proposals.VoteValue.No ? weight : 0,
      value == Proposals.VoteValue.Abstain ? weight : 0
    );
    return true;
  }

  /**
   * @notice Votes partially on a proposal in the referendum stage.
   * @param proposalId The ID of the proposal to vote on.
