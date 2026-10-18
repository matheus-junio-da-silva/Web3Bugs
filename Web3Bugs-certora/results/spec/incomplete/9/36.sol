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

// Original: contracts/9/specs/harnesses/GovernanceHarness.sol:20-55 (function getNoneVoteEnum)
  function getNoneVoteEnum() public pure returns (uint256) {
    return uint256(VoteValue.None);
  }
  function getAbstainVoteEnum() public pure returns (uint256) {
    return uint256(VoteValue.Abstain);
  }
  function getYesVoteEnum() public pure returns (uint256) {
    return uint256(VoteValue.Yes);
  }
  function getNoVoteEnum() public pure returns (uint256) {
    return uint256(VoteValue.No);
  }

  /* Override */
  LockedGoldHarness lockedGold;
  function getLockedGold() internal view returns (ILockedGold) {
    return lockedGold;
  }

  function getTotalLockedGold() public view returns (uint256) {
    return lockedGold.getTotalLockedGold();
  }

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

// Original: contracts/9/contracts/common/Accounts.sol:857-892 (function getVoteSigner)
  function getVoteSigner(address account) public view returns (address) {
    return getLegacySigner(account, VoteSigner);
  }

  /**
   * @notice Returns the validator signer for the specified account.
   * @param account The address of the account.
   * @return The address with which the account can register a validator or group.
   */
  function getValidatorSigner(address account) public view returns (address) {
    return getLegacySigner(account, ValidatorSigner);
  }

  /**
   * @notice Returns the attestation signer for the specified account.
   * @param account The address of the account.
   * @return The address with which the account can sign attestations.
   */
  function getAttestationSigner(address account) public view returns (address) {
    return getLegacySigner(account, AttestationSigner);
  }

  /**
   * @notice Checks whether or not the account has an indexed signer
   * registered for one of the legacy roles
   */
  function hasLegacySigner(address account, bytes32 role) public view returns (bool) {
    return getLegacySigner(account, role) != account;
  }

  /**
   * @notice Checks whether or not the account has an indexed signer
   * registered for a role
   */
  function hasDefaultSigner(address account, bytes32 role) public view returns (bool) {
    return getDefaultSigner(account, role) != account;
