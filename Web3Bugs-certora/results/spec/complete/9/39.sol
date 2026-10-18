// Original: contracts/9/contracts/governance/Governance.sol:1076-1111 (function isApproved)
  function isApproved(uint256 proposalId) external view returns (bool) {
    return proposals[proposalId].isApproved();
  }

  /**
   * @notice Returns the referendum vote totals for a proposal.
   * @param proposalId The ID of the proposal.
   * @return yes The yes vote totals.
   * @return no The no vote totals.
   * @return abstain The abstain vote totals.
   */
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

// Original: contracts/9/contracts/governance/Governance.sol:1343-1378 (function isDequeuedProposalExpired)
  function isDequeuedProposalExpired(uint256 proposalId) external view returns (bool) {
    Proposals.Proposal storage proposal = proposals[proposalId];
    return _isDequeuedProposalExpired(proposal, getProposalDequeuedStage(proposal));
  }

  /**
   * @notice Returns whether or not a dequeued proposal has expired.
   * @param proposal The proposal struct.
   * @return Whether or not the dequeued proposal has expired.
   */
  function _isDequeuedProposalExpired(Proposals.Proposal storage proposal, Proposals.Stage stage)
    private
    view
    returns (bool)
  {
    // The proposal is considered expired under the following conditions:
    //   1. Past the referendum stage and not passing.
    //   2. Past the execution stage.
    return ((stage > Proposals.Stage.Execution) ||
      (stage > Proposals.Stage.Referendum && !_isProposalPassing(proposal)));
  }

  /**
   * @notice Returns whether or not a queued proposal has expired.
   * @param proposalId The ID of the proposal.
   * @return Whether or not the dequeued proposal has expired.
   */
  function isQueuedProposalExpired(uint256 proposalId) public view returns (bool) {
    return _isQueuedProposalExpired(proposals[proposalId]);
  }

  /**
   * @notice Returns whether or not a queued proposal has expired.
   * @param proposal The proposal struct.
   * @return Whether or not the dequeued proposal has expired.
   */

// Original: contracts/9/contracts/governance/Governance.sol:614-649 (function approve)
  function approve(uint256 proposalId, uint256 index) external onlyApprover returns (bool) {
    dequeueProposalsIfReady();
    (Proposals.Proposal storage proposal, Proposals.Stage stage) = requireDequeuedAndDeleteExpired(
      proposalId,
      index
    );
    if (!proposal.exists()) {
      return false;
    }

    require(!proposal.isApproved(), "Proposal already approved");
    require(
      stage == Proposals.Stage.Referendum || stage == Proposals.Stage.Execution,
      "Proposal not in correct stage"
    );
    proposal.approved = true;
    // Ensures networkWeight is set by the end of the Referendum stage, even if 0 votes are cast.
    proposal.networkWeight = getLockedGold().getTotalLockedGold();
    emit ProposalApproved(proposalId);
    return true;
  }

  /**
   * @notice Votes on a proposal in the referendum stage.
   * @param proposalId The ID of the proposal to vote on.
   * @param index The index of the proposal ID in `dequeued`.
   * @param value Whether to vote yes, no, or abstain.
   * @return Whether or not the vote was cast successfully.
   */
  /* solhint-disable code-complexity */
  function vote(uint256 proposalId, uint256 index, Proposals.VoteValue value)
    external
    nonReentrant
    returns (bool)
  {
    dequeueProposalsIfReady();

// Original: contracts/9/contracts/governance/Proposals.sol:306-341 (function isApproved)
  function isApproved(Proposal storage proposal) internal view returns (bool) {
    return proposal.approved;
  }

  /**
   * @notice Returns whether or not a proposal exists.
   * @param proposal The proposal struct.
   * @return Whether or not the proposal exists.
   */
  function exists(Proposal storage proposal) internal view returns (bool) {
    return proposal.timestamp > 0;
  }

  // call has been separated into its own function in order to take advantage
  // of the Solidity's code generator to produce a loop that copies tx.data into memory.
  /**
   * @notice Executes a function call.
   * @param value The value of CELO to be sent with the function call.
   * @param destination The destination address of the function call.
   * @param dataLength The length of the data to be included in the function call.
   * @param data The data to be included in the function call.
   */
  function externalCall(address destination, uint256 value, uint256 dataLength, bytes memory data)
    private
    returns (bool)
  {
    bool result;

    if (dataLength > 0) require(Address.isContract(destination), "Invalid contract address");

    /* solhint-disable no-inline-assembly */
    assembly {
      /* solhint-disable max-line-length */
      let x := mload(0x40) // "Allocate" memory for output (0x40 is where "free memory" pointer is stored by convention)
      let d := add(data, 32) // First 32 bytes are the padded length of data, so exclude that
      result := call(
