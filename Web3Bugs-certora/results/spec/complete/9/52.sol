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

// Original: contracts/9/contracts/governance/LockedGold.sol:197-226 (decrementNonvotingAccountBalance)
  function decrementNonvotingAccountBalance(address account, uint256 value)
    external
    onlyRegisteredContract(ELECTION_REGISTRY_ID)
  {
    _decrementNonvotingAccountBalance(account, value);
  }

  /**
   * @notice Increments the non-voting balance for an account.
   * @param account The account whose non-voting balance should be incremented.
   * @param value The amount by which to increment.
   */
  function _incrementNonvotingAccountBalance(address account, uint256 value) private {
    balances[account].nonvoting = balances[account].nonvoting.add(value);
    totalNonvoting = totalNonvoting.add(value);
  }

  /**
   * @notice Decrements the non-voting balance for an account.
   * @param account The account whose non-voting balance should be decremented.
   * @param value The amount by which to decrement.
   */
  function _decrementNonvotingAccountBalance(address account, uint256 value) private {
    balances[account].nonvoting = balances[account].nonvoting.sub(value);
    totalNonvoting = totalNonvoting.sub(value);
  }

  /**
   * @notice Unlocks gold that becomes withdrawable after the unlocking period.
   * @param value The amount of gold to unlock.

// Original: contracts/9/contracts/governance/LockedGold.sol:184-213 (incrementNonvotingAccountBalance)
  function incrementNonvotingAccountBalance(address account, uint256 value)
    external
    onlyRegisteredContract(ELECTION_REGISTRY_ID)
  {
    _incrementNonvotingAccountBalance(account, value);
  }

  /**
   * @notice Decrements the non-voting balance for an account.
   * @param account The account whose non-voting balance should be decremented.
   * @param value The amount by which to decrement.
   * @dev Can only be called by the registered "Election" smart contract.
   */
  function decrementNonvotingAccountBalance(address account, uint256 value)
    external
    onlyRegisteredContract(ELECTION_REGISTRY_ID)
  {
    _decrementNonvotingAccountBalance(account, value);
  }

  /**
   * @notice Increments the non-voting balance for an account.
   * @param account The account whose non-voting balance should be incremented.
   * @param value The amount by which to increment.
   */
  function _incrementNonvotingAccountBalance(address account, uint256 value) private {
    balances[account].nonvoting = balances[account].nonvoting.add(value);
    totalNonvoting = totalNonvoting.add(value);
  }

