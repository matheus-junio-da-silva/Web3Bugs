// Original: contracts/9/contracts/governance/LockedGold.sol:139-168 (initialize)
  function initialize(address registryAddress, uint256 _unlockingPeriod) external initializer {
    _transferOwnership(msg.sender);
    setRegistry(registryAddress);
    setUnlockingPeriod(_unlockingPeriod);
    maxDelegateesCount = 10;
  }

  /**
   * @notice Sets the duration in seconds users must wait before withdrawing gold after unlocking.
   * @param value The unlocking period in seconds.
   */
  function setUnlockingPeriod(uint256 value) public onlyOwner {
    require(value != unlockingPeriod, "Unlocking period not changed");
    unlockingPeriod = value;
    emit UnlockingPeriodSet(value);
  }

  /**
   * @notice Sets max delegatees count.
   * @param value The max delegatees count.
   */
  function setMaxDelegateesCount(uint256 value) public onlyOwner {
    maxDelegateesCount = value;
    emit MaxDelegateesCountSet(value);
  }

  /**
   * @notice Locks gold to be used for voting.
   */
  function lock() external payable nonReentrant {
