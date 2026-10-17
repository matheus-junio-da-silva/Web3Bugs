// Original: contracts/9/contracts/governance/LockedGold.sol:289-307 (locked-gold withdrawal with account and maturity guards)
  /**
   * @notice Withdraws gold that has been unlocked after the unlocking period has passed.
   * @param index The index of the pending withdrawal to withdraw.
   */
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

// Original: contracts/9/specs/harnesses/LockedGoldHarness.sol:18-29 (native balance observation and pending amount)
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
