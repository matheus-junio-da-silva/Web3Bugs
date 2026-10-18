// Original: contracts/9/contracts/governance/Governance.sol:1131-1166 (function getUpvotes)
  function getUpvotes(uint256 proposalId) external view returns (uint256) {
    require(isQueued(proposalId), "Proposal not queued");
    return queue.getValue(proposalId);
  }

  /**
   * @notice Returns the proposal ID and upvote total for all queued proposals.
   * @return proposalID The proposal ID for all queued proposals.
   * @return total The upvote total for all queued proposals.
   * @dev Note that this includes expired proposals that have yet to be removed from the queue.
   */
  function getQueue() external view returns (uint256[] memory, uint256[] memory) {
    return queue.getElements();
  }

  /**
   * @notice Returns the dequeued proposal IDs.
   * @return The dequeued proposal IDs.
   * @dev Note that this includes unused indices with proposalId == 0 from deleted proposals.
   */
  function getDequeue() external view returns (uint256[] memory) {
    return dequeued;
  }

  /**
   * @notice Returns the ID of the proposal upvoted by `account` and the weight of that upvote.
   * @param account The address of the account.
   * @return The ID of the proposal upvoted by `account`.
   * @return The weight of that upvote.
   */
  function getUpvoteRecord(address account) external view returns (uint256, uint256) {
    UpvoteRecord memory upvoteRecord = voters[account].upvote;
    return (upvoteRecord.proposalId, upvoteRecord.weight);
  }

  /**

// Original: contracts/9/contracts/governance/Governance.sol:530-565 (function upvote)
  function upvote(uint256 proposalId, uint256 lesser, uint256 greater)
    external
    nonReentrant
    returns (bool)
  {
    dequeueProposalsIfReady();
    // If acting on an expired proposal, expire the proposal and take no action.
    if (removeIfQueuedAndExpired(proposalId)) {
      return false;
    }

    address account = getAccounts().voteSignerToAccount(msg.sender);
    Voter storage voter = voters[account];
    removeIfQueuedAndExpired(voter.upvote.proposalId);

    // We can upvote a proposal in the queue if we're not already upvoting a proposal in the queue.
    uint256 weight = getLockedGold().getAccountTotalLockedGold(account);
    require(weight > 0, "cannot upvote without locking gold");
    require(queue.contains(proposalId), "cannot upvote a proposal not in the queue");
    require(
      voter.upvote.proposalId == 0 || !queue.contains(voter.upvote.proposalId),
      "cannot upvote more than one queued proposal"
    );
    uint256 upvotes = queue.getValue(proposalId).add(weight);
    queue.update(proposalId, upvotes, lesser, greater);
    voter.upvote = UpvoteRecord(proposalId, weight);
    emit ProposalUpvoted(proposalId, account, weight);
    return true;
  }

  /**
   * @notice Returns stage of governance process given proposal is in
   * @param proposalId The ID of the proposal to query.
   * @return proposal stage
   */
  function getProposalStage(uint256 proposalId) external view returns (Proposals.Stage) {

// Original: contracts/9/contracts/governance/Governance.sol:1161-1196 (function getUpvoteRecord)
  function getUpvoteRecord(address account) external view returns (uint256, uint256) {
    UpvoteRecord memory upvoteRecord = voters[account].upvote;
    return (upvoteRecord.proposalId, upvoteRecord.weight);
  }

  /**
   * @notice Returns the ID of the most recently dequeued proposal voted on by `account`.
   * @param account The address of the account.
   * @return The ID of the most recently dequeued proposal voted on by `account`..
   */
  function getMostRecentReferendumProposal(address account) external view returns (uint256) {
    return voters[account].mostRecentReferendumProposal;
  }

  /**
   * @notice Returns number of validators from current set which have whitelisted the given hotfix.
   * @param hash The abi encoded keccak256 hash of the hotfix transaction.
   * @return Whitelist tally
   */
  function hotfixWhitelistValidatorTally(bytes32 hash) public view returns (uint256) {
    uint256 tally = 0;
    uint256 n = numberValidatorsInCurrentSet();
    IAccounts accounts = getAccounts();
    for (uint256 i = 0; i < n; i = i.add(1)) {
      address validatorSigner = validatorSignerAddressFromCurrentSet(i);
      address validatorAccount = accounts.signerToAccount(validatorSigner);
      if (
        isHotfixWhitelistedBy(hash, validatorSigner) ||
        isHotfixWhitelistedBy(hash, validatorAccount)
      ) {
        tally = tally.add(1);
      }
    }
    return tally;
  }


// Original: contracts/9/specs/harnesses/GovernanceHarness.sol:43-66 (function getUpvotedProposal)
  function getUpvotedProposal(address account) public view returns (uint256) {
    uint256 proposalId;
    uint256 weight;
    (proposalId, weight) = this.getUpvoteRecord(account);
    return proposalId;
  }

  function getProposalSlim(uint256 proposalId)
    external
    view
    returns (address, uint256, uint256, uint256)
  {
    Proposals.Proposal storage proposal = proposals[proposalId];
    return (proposal.proposer, proposal.deposit, proposal.timestamp, proposal.transactions.length);
  }

  function getVotedId(address account, uint256 index) external view returns (uint256) {
    return voters[account].referendumVotes[index].proposalId;
  }

  // override for performance - do nothing
  function dequeueProposalsIfReady() public {}
}
