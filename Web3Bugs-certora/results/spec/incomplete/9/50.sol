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
