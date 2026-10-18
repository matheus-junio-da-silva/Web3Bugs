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
