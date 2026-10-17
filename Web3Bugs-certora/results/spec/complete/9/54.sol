// Original: contracts/9/contracts/governance/LockedGold.sol:293-322 (withdraw)
  function withdraw(uint256 index) external nonReentrant {
    require(
      getAccounts().isAccount(msg.sender),
      "Sender must be registered with Account.createAccount to withdraw"
    );
    Balances storage account = balances[msg.sender];
    require(index < account.pendingWithdrawals.length, "Bad pending withdrawal index");
    PendingWithdrawal storage pendingWithdrawal = account.pendingWithdrawals[index];
    require(now >= pendingWithdrawal.timestamp, "Pending withdrawal not available");
    uint256 value = pendingWithdrawal.value;
    deletePendingWithdrawal(account.pendingWithdrawals, index);
    require(value <= address(this).balance, "Inconsistent balance");
    msg.sender.sendValue(value);
    emit GoldWithdrawn(msg.sender, value);
  }

  /**
   * @notice Returns the total amount of locked gold in the system. Note that this does not include
   *   gold that has been unlocked but not yet withdrawn.
   * @return The total amount of locked gold in the system.
   */
  function getTotalLockedGold() external view returns (uint256) {
    return totalNonvoting.add(getElection().getTotalVotes());
  }

  /**
   * @notice Returns the total amount of locked gold not being used to vote in elections.
   * @return The total amount of locked gold not being used to vote in elections.
   */
  function getNonvotingLockedGold() external view returns (uint256) {

// Original: contracts/9/specs/harnesses/LockedGoldHarness.sol:18-47 (ercBalanceOf)
  function ercBalanceOf(address a) public returns (uint256) {
    return a.balance;
  }

  function getPendingWithdrawalsIndex(address account, uint256 index) public returns (uint256) {
    require(getAccounts().isAccount(account), "Unknown account");
    require(
      index < balances[account].pendingWithdrawals.length,
      "Index cannot exceed pending withdrawals length"
    );
    return balances[account].pendingWithdrawals[index].value;
  }

  function getunlockingPeriod() public returns (uint256) {
    return unlockingPeriod;
  }

  function getTotalPendingWithdrawals(address account) public view returns (uint256) {
    require(getAccounts().isAccount(account), "Unknown account");
    uint256 length = balances[account].pendingWithdrawals.length;
    uint256 total = 0;
    for (uint256 i = 0; i < length; i = i.add(1)) {
      uint256 pendingValue = balances[account].pendingWithdrawals[i].value;
      require(total.add(pendingValue) >= total, "Pending value must be greater than 0");
      total = total.add(pendingValue);
    }
    return total;
  }

  function pendingWithdrawalsNotFull(address account) public view returns (bool) {

// Original: contracts/9/specs/harnesses/LockedGoldHarness.sol:22-51 (getPendingWithdrawalsIndex)
  function getPendingWithdrawalsIndex(address account, uint256 index) public returns (uint256) {
    require(getAccounts().isAccount(account), "Unknown account");
    require(
      index < balances[account].pendingWithdrawals.length,
      "Index cannot exceed pending withdrawals length"
    );
    return balances[account].pendingWithdrawals[index].value;
  }

  function getunlockingPeriod() public returns (uint256) {
    return unlockingPeriod;
  }

  function getTotalPendingWithdrawals(address account) public view returns (uint256) {
    require(getAccounts().isAccount(account), "Unknown account");
    uint256 length = balances[account].pendingWithdrawals.length;
    uint256 total = 0;
    for (uint256 i = 0; i < length; i = i.add(1)) {
      uint256 pendingValue = balances[account].pendingWithdrawals[i].value;
      require(total.add(pendingValue) >= total, "Pending value must be greater than 0");
      total = total.add(pendingValue);
    }
    return total;
  }

  function pendingWithdrawalsNotFull(address account) public view returns (bool) {
    return balances[account].pendingWithdrawals.length.add(2) >= 2; // we can add 2 more additional elements
  }

  function getPendingWithdrawalsLength(address account) external view returns (uint256) {

// Original: contracts/9/contracts/governance/Governance.sol:972-1001 (withdraw)
  function withdraw() external nonReentrant returns (bool) {
    uint256 value = refundedDeposits[msg.sender];
    require(value != 0, "Nothing to withdraw");
    require(value <= address(this).balance, "Inconsistent balance");
    refundedDeposits[msg.sender] = 0;
    msg.sender.sendValue(value);
    return true;
  }

  /**
   * @notice Returns whether or not a particular account is voting on proposals.
   * @param account The address of the account.
   * @return Whether or not the account is voting on proposals.
   */
  function isVoting(address account) external view returns (bool) {
    Voter storage voter = voters[account];
    uint256 upvotedProposal = voter.upvote.proposalId;
    bool isVotingQueue = upvotedProposal != 0 &&
      isQueued(upvotedProposal) &&
      !isQueuedProposalExpired(upvotedProposal);
    Proposals.Proposal storage proposal = proposals[voter.mostRecentReferendumProposal];
    bool isVotingReferendum = (getProposalDequeuedStage(proposal) == Proposals.Stage.Referendum);
    return isVotingQueue || isVotingReferendum;
  }

  /**
   * @notice Returns the number of seconds proposals stay in the referendum stage.
   * @return The number of seconds proposals stay in the referendum stage.
   */
  function getReferendumStageDuration() external view returns (uint256) {
