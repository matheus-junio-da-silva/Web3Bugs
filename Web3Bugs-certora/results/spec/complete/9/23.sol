// Original: contracts/9/contracts/common/Accounts.sol:866-893 (relevant getValidatorSigner)
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
  }

  /**
   * @notice Checks whether or not the account has an indexed signer
   * registered for a role
   */
  function hasDefaultSigner(address account, bytes32 role) public view returns (bool) {
    return getDefaultSigner(account, role) != account;
  }

// Original: contracts/9/contracts/common/Accounts.sol:771-798 (relevant validatorSignerToAccount)
  function validatorSignerToAccount(address signer) public view returns (address) {
    return signerToAccountWithRole(signer, ValidatorSigner);
  }

  /**
   * @notice Returns the account associated with `signer`.
   * @param signer The address of the account or currently authorized vote signer.
   * @dev Fails if the `signer` is not an account or currently authorized vote signer.
   * @return The associated account that signer is authorized to vote for.
   */
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

// Original: contracts/9/specs/harnesses/AccountsHarness.sol:52-62 (relevant _getValidatorRole)
  function _getValidatorRole() public view returns (bytes32) {
    return ValidatorSigner;
  }
  function _getVoteRole() public view returns (bytes32) {
    return VoteSigner;
  }
  function _getAttestationRole() public view returns (bytes32) {
    return AttestationSigner;
  }
}

