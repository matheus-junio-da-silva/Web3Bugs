// Original: contracts/9/contracts/common/Accounts.sol:857-884 (relevant getVoteSigner)
  function getVoteSigner(address account) public view returns (address) {
    return getLegacySigner(account, VoteSigner);
  }

  /**
   * @notice Returns the validator signer for the specified account.
   * @param account The address of the account.
   * @return The address with which the account can register a validator or group.
   */
  function getValidatorSigner(address account) public view returns (address) {
    return getLegacySigner(account, ValidatorSigner);
  }

  /**
   * @notice Returns the attestation signer for the specified account.
   * @param account The address of the account.
   * @return The address with which the account can sign attestations.
   */
  function getAttestationSigner(address account) public view returns (address) {
    return getLegacySigner(account, AttestationSigner);
  }

  /**
   * @notice Checks whether or not the account has an indexed signer
   * registered for one of the legacy roles
   */
  function hasLegacySigner(address account, bytes32 role) public view returns (bool) {
    return getLegacySigner(account, role) != account;

// Original: contracts/9/contracts/common/Accounts.sol:781-808 (relevant voteSignerToAccount)
  function voteSignerToAccount(address signer) external view returns (address) {
    return signerToAccountWithRole(signer, VoteSigner);
  }

  /**
   * @notice Returns the account associated with `signer`.
   * @param signer The address of the account or previously authorized signer.
   * @dev Fails if the `signer` is not an account or previously authorized signer.
   * @return The associated account.
   */
  function signerToAccount(address signer) external view returns (address) {
    address authorizingAccount = authorizedBy[signer];
    if (authorizingAccount != address(0)) {
      return authorizingAccount;
    } else {
      require(isAccount(signer), "Must first register address with Account.createAccount");
      return signer;
    }
  }

  /**
   * @notice Checks whether the role is one of Vote, Validator or Attestation
   * @param role The role to check
   */
  function isLegacyRole(bytes32 role) public pure returns (bool) {
    return role == VoteSigner || role == ValidatorSigner || role == AttestationSigner;
  }


// Original: contracts/9/specs/harnesses/AccountsHarness.sol:55-62 (relevant _getVoteRole)
  function _getVoteRole() public view returns (bytes32) {
    return VoteSigner;
  }
  function _getAttestationRole() public view returns (bytes32) {
    return AttestationSigner;
  }
}
