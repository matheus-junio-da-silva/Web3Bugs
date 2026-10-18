// Original: contracts/9/contracts/common/Accounts.sol:875-902 (relevant getAttestationSigner)
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

  /**
   * @notice Checks whether or not the account has an indexed signer
   * registered for the role
   */
  function hasIndexedSigner(address account, bytes32 role) public view returns (bool) {
    return isLegacyRole(role) ? hasLegacySigner(account, role) : hasDefaultSigner(account, role);
  }


// Original: contracts/9/contracts/common/Accounts.sol:761-788 (relevant attestationSignerToAccount)
  function attestationSignerToAccount(address signer) external view returns (address) {
    return signerToAccountWithRole(signer, AttestationSigner);
  }

  /**
   * @notice Returns the account associated with `signer`.
   * @param signer The address of an account or currently authorized validator signer.
   * @dev Fails if the `signer` is not an account or currently authorized validator.
   * @return The associated account that signer is authorized to validate for.
   */
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

// Original: contracts/9/specs/harnesses/AccountsHarness.sol:58-62 (relevant _getAttestationRole)
  function _getAttestationRole() public view returns (bytes32) {
    return AttestationSigner;
  }
}
