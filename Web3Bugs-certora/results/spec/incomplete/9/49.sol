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

// Original: contracts/9/contracts/governance/Proposals.sol:293-328 (function getVoteTotals)
  function getVoteTotals(Proposal storage proposal)
    internal
    view
    returns (uint256, uint256, uint256)
  {
    return (proposal.votes.yes, proposal.votes.no, proposal.votes.abstain);
  }

  /**
   * @notice Returns whether or not a proposal has been approved.
   * @param proposal The proposal struct.
   * @return Whether or not the proposal has been approved.
   */
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

// Original: contracts/9/specs/harnesses/GovernanceHarness.sol:39-66 (function getTotalLockedGold)
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
    return (proposal.proposer, proposal.deposit, proposal.timestamp, proposal.transactions.length);
  }

  function getVotedId(address account, uint256 index) external view returns (uint256) {
    return voters[account].referendumVotes[index].proposalId;
  }

  // override for performance - do nothing
  function dequeueProposalsIfReady() public {}
}
