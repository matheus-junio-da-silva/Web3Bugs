// Original: contracts/9/specs/harnesses/GovernanceHarness.sol:15-50 (function getFromDequeued)
  function getFromDequeued(uint256 index) public view returns (uint256) {
    return dequeued[index]; // note that this can revert if index is unchecked
  }

  // VoteValue
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

// Original: contracts/9/specs/harnesses/GovernanceHarness.sol:11-46 (function getDequeuedLength)
  function getDequeuedLength() public view returns (uint256) {
    return dequeued.length;
  }

  function getFromDequeued(uint256 index) public view returns (uint256) {
    return dequeued[index]; // note that this can revert if index is unchecked
  }

  // VoteValue
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

// Original: contracts/9/specs/harnesses/GovernanceHarness.sol:50-66 (function getProposalSlim)
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

