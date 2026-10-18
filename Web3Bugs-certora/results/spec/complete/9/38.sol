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
