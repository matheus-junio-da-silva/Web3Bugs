// Original: contracts/9/contracts/governance/Governance.sol:440-475 (function setConstitution)
  function setConstitution(address destination, bytes4 functionId, uint256 threshold)
    external
    onlyOwner
  {
    require(destination != address(0), "Destination cannot be zero");
    require(
      threshold > FIXED_HALF && threshold <= FixidityLib.fixed1().unwrap(),
      "Threshold has to be greater than majority and not greater than unanimity"
    );
    if (functionId == 0) {
      constitution[destination].defaultThreshold = FixidityLib.wrap(threshold);
    } else {
      constitution[destination].functionThresholds[functionId] = FixidityLib.wrap(threshold);
    }
    emit ConstitutionSet(destination, functionId, threshold);
  }

  /**
   * @notice Creates a new proposal and adds it to end of the queue with no upvotes.
   * @param values The values of CELO to be sent in the proposed transactions.
   * @param destinations The destination addresses of the proposed transactions.
   * @param data The concatenated data to be included in the proposed transactions.
   * @param dataLengths The lengths of each transaction's data.
   * @return The ID of the newly proposed proposal.
   * @dev The minimum deposit must be included with the proposal, returned if/when the proposal is
   *   dequeued.
   */
  function propose(
    uint256[] calldata values,
    address[] calldata destinations,
    bytes calldata data,
    uint256[] calldata dataLengths,
    string calldata descriptionUrl
  ) external payable returns (uint256) {
    dequeueProposalsIfReady();
    require(msg.value >= minDeposit, "Too small deposit");

// Original: contracts/9/contracts/governance/Governance.sol:1435-1470 (function getConstitution)
  function getConstitution(address destination, bytes4 functionId) external view returns (uint256) {
    return _getConstitution(destination, functionId).unwrap();
  }

  function _getConstitution(address destination, bytes4 functionId)
    internal
    view
    returns (FixidityLib.Fraction memory)
  {
    // Default to a simple majority.
    FixidityLib.Fraction memory threshold = FixidityLib.wrap(FIXED_HALF);
    if (constitution[destination].functionThresholds[functionId].unwrap() != 0) {
      threshold = constitution[destination].functionThresholds[functionId];
    } else if (constitution[destination].defaultThreshold.unwrap() != 0) {
      threshold = constitution[destination].defaultThreshold;
    }
    return threshold;
  }

  /**
   * @notice Returns max number of votes cast by an account.
   * @param account The address of the account.
   * @return The total number of votes cast by an account.
   */
  function getAmountOfGoldUsedForVoting(address account) public view returns (uint256) {
    Voter storage voter = voters[account];

    uint256 upvotedProposalId = voter.upvote.proposalId;
    bool isVotingQueue = upvotedProposalId != 0 &&
      isQueued(upvotedProposalId) &&
      !isQueuedProposalExpired(upvotedProposalId);

    if (isVotingQueue) {
      uint256 weight = getLockedGold().getAccountTotalLockedGold(account);
      return weight;
    }
