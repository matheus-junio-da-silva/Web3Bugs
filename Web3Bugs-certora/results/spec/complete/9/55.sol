// Original: contracts/9/contracts/governance/LockedGold.sol:228-257 (unlock)
  function unlock(uint256 value) external nonReentrant {
    require(
      getAccounts().isAccount(msg.sender),
      "Sender must be registered with Account.createAccount to lock or unlock"
    );
    Balances storage account = balances[msg.sender];

    uint256 totalLockedGold = getAccountTotalLockedGold(msg.sender);
    // Prevent unlocking gold when voting on governance proposals so that the gold cannot be
    // used to vote more than once.
    uint256 remainingLockedGold = totalLockedGold.sub(value);

    uint256 totalReferendumVotes = getGovernance().getAmountOfGoldUsedForVoting(msg.sender);
    require(
      remainingLockedGold >= totalReferendumVotes,
      "Not enough unlockable celo. Celo is locked in voting."
    );

    FixidityLib.Fraction memory delegatedPercentage = delegatorInfo[msg.sender]
      .totalDelegatedCeloFraction;

    if (FixidityLib.gt(delegatedPercentage, FixidityLib.newFixed(0))) {
      revokeFromDelegatedWhenUnlocking(msg.sender, value);
    }

    uint256 balanceRequirement = getValidators().getAccountLockedGoldRequirement(msg.sender);
    require(
      balanceRequirement == 0 || balanceRequirement <= remainingLockedGold,
      "Either account doesn't have enough locked Celo or locked Celo is being used for voting."
    );

// Original: contracts/9/contracts/governance/LockedGold.sol:786-815 (getTotalPendingWithdrawals)
  function getTotalPendingWithdrawals(address account) external view returns (uint256) {
    uint256 pendingWithdrawalSum = 0;
    PendingWithdrawal[] memory withdrawals = balances[account].pendingWithdrawals;
    for (uint256 i = 0; i < withdrawals.length; i = i.add(1)) {
      pendingWithdrawalSum = pendingWithdrawalSum.add(withdrawals[i].value);
    }
    return pendingWithdrawalSum;
  }

  function getSlashingWhitelist() external view returns (bytes32[] memory) {
    return slashingWhitelist;
  }

  /**
   * @notice Deletes a pending withdrawal.
   * @param list The list of pending withdrawals from which to delete.
   * @param index The index of the pending withdrawal to delete.
   */
  function deletePendingWithdrawal(PendingWithdrawal[] storage list, uint256 index) private {
    uint256 lastIndex = list.length.sub(1);
    list[index] = list[lastIndex];
    list.length = lastIndex;
  }

  /**
   * @notice Adds `slasher` to whitelist of approved slashing addresses.
   * @param slasherIdentifier Identifier to whitelist.
   */
  function addSlasher(string calldata slasherIdentifier) external onlyOwner {
    bytes32 keyBytes = keccak256(abi.encodePacked(slasherIdentifier));

// Original: contracts/9/contracts/governance/LockedGold.sol:720-749 (getAccountNonvotingLockedGold)
  function getAccountNonvotingLockedGold(address account) external view returns (uint256) {
    return balances[account].nonvoting;
  }

  /**
   * @notice Returns the pending withdrawals from unlocked gold for an account.
   * @param account The address of the account.
   * @return The value for each pending withdrawal.
   * @return The timestamp for each pending withdrawal.
   */
  function getPendingWithdrawals(address account)
    external
    view
    returns (uint256[] memory, uint256[] memory)
  {
    require(
      getAccounts().isAccount(account),
      "Unknown account: only registered accounts have pending withdrawals"
    );
    uint256 length = balances[account].pendingWithdrawals.length;
    uint256[] memory values = new uint256[](length);
    uint256[] memory timestamps = new uint256[](length);
    for (uint256 i = 0; i < length; i = i.add(1)) {
      PendingWithdrawal memory pendingWithdrawal = (balances[account].pendingWithdrawals[i]);
      values[i] = pendingWithdrawal.value;
      timestamps[i] = pendingWithdrawal.timestamp;
    }
    return (values, timestamps);
  }


// Original: contracts/9/specs/harnesses/LockedGoldHarness.sol:47-64 (pendingWithdrawalsNotFull)
  function pendingWithdrawalsNotFull(address account) public view returns (bool) {
    return balances[account].pendingWithdrawals.length.add(2) >= 2; // we can add 2 more additional elements
  }

  function getPendingWithdrawalsLength(address account) external view returns (uint256) {
    uint256 length = balances[account].pendingWithdrawals.length;
    return length;
  }

  function getGoldToken() internal view returns (IERC20) {
    return IERC20(goldToken);
  }

  function getGoldTokenExt() public view returns (address) {
    return address(goldToken);
  }
}

