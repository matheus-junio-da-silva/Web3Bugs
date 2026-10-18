// Original: contracts/9/contracts/governance/Governance.sol:1034-1069 (function proposalExists)
  function proposalExists(uint256 proposalId) external view returns (bool) {
    return proposals[proposalId].exists();
  }

  /**
   * @notice Returns an unpacked proposal struct with its transaction count.
   * @param proposalId The ID of the proposal to unpack.
   * @return proposer
   * @return deposit
   * @return timestamp
   * @return transaction Transaction count.
   * @return description Description url.
   */
  function getProposal(uint256 proposalId)
    external
    view
    returns (address, uint256, uint256, uint256, string memory, uint256, bool)
  {
    return proposals[proposalId].unpack();
  }

  /**
   * @notice Returns a specified transaction in a proposal.
   * @param proposalId The ID of the proposal to query.
   * @param index The index of the specified transaction in the proposal's transaction list.
   * @return value Transaction value.
   * @return destination Transaction destination.
   * @return data Transaction data.
   */
  function getProposalTransaction(uint256 proposalId, uint256 index)
    external
    view
    returns (uint256, address, bytes memory)
  {
    return proposals[proposalId].getTransaction(index);
  }

// Original: contracts/9/specs/harnesses/GovernanceHarness.sol:59-66 (function getVotedId)
  function getVotedId(address account, uint256 index) external view returns (uint256) {
    return voters[account].referendumVotes[index].proposalId;
  }

  // override for performance - do nothing
  function dequeueProposalsIfReady() public {}
}
