// Original: contracts/9/contracts/governance/Governance.sol:1161-1196 (function getUpvoteRecord)
  function getUpvoteRecord(address account) external view returns (uint256, uint256) {
    UpvoteRecord memory upvoteRecord = voters[account].upvote;
    return (upvoteRecord.proposalId, upvoteRecord.weight);
  }

  /**
   * @notice Returns the ID of the most recently dequeued proposal voted on by `account`.
   * @param account The address of the account.
   * @return The ID of the most recently dequeued proposal voted on by `account`..
   */
  function getMostRecentReferendumProposal(address account) external view returns (uint256) {
    return voters[account].mostRecentReferendumProposal;
  }

  /**
   * @notice Returns number of validators from current set which have whitelisted the given hotfix.
   * @param hash The abi encoded keccak256 hash of the hotfix transaction.
   * @return Whitelist tally
   */
  function hotfixWhitelistValidatorTally(bytes32 hash) public view returns (uint256) {
    uint256 tally = 0;
    uint256 n = numberValidatorsInCurrentSet();
    IAccounts accounts = getAccounts();
    for (uint256 i = 0; i < n; i = i.add(1)) {
      address validatorSigner = validatorSignerAddressFromCurrentSet(i);
      address validatorAccount = accounts.signerToAccount(validatorSigner);
      if (
        isHotfixWhitelistedBy(hash, validatorSigner) ||
        isHotfixWhitelistedBy(hash, validatorAccount)
      ) {
        tally = tally.add(1);
      }
    }
    return tally;
  }

