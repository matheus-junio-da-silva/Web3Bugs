// Original: contracts/9/contracts/governance/LockedGold.sol:322-351 (getNonvotingLockedGold)
  function getNonvotingLockedGold() external view returns (uint256) {
    return totalNonvoting;
  }

  /**
   * Delegates CELO to delegatee.
   * @param delegatee The delegatee account.
   * @param delegateFraction Fraction of total CELO that will be delegated from delegatee. Fixidity fraction
   */
  function delegateGovernanceVotes(address delegatee, uint256 delegateFraction) external {
    FixidityLib.Fraction memory percentageToDelegate = FixidityLib.wrap(delegateFraction);
    require(
      FixidityLib.lte(percentageToDelegate, FixidityLib.fixed1()),
      "Delegate fraction must be less than or equal to 1"
    );
    address delegatorAccount = getAccounts().voteSignerToAccount(msg.sender);
    address delegateeAccount = getAccounts().voteSignerToAccount(delegatee);

    IValidators validators = getValidators();
    require(!validators.isValidator(delegatorAccount), "Validators cannot delegate votes.");
    require(
      !validators.isValidatorGroup(delegatorAccount),
      "Validator groups cannot delegate votes."
    );

    Delegated storage delegated = delegatorInfo[delegatorAccount];
    delegated.delegatees.add(delegateeAccount);
    require(delegated.delegatees.length() <= maxDelegateesCount, "Too many delegatees");

    DelegatedInfo storage currentDelegateeInfo = delegated

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

