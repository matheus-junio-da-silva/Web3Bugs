// Original: contracts/9/contracts/common/Accounts.sol:1009-1036 (relevant isAccount)
  function isAccount(address account) public view returns (bool) {
    return (accounts[account].exists);
  }

  /**
   * @notice Check if an account already exists.
   * @param account The address of the account
   * @return Returns `false` if account exists. Returns `true` otherwise.
   */
  function isNotAccount(address account) internal view returns (bool) {
    return (!accounts[account].exists);
  }

  /**
   * @notice Check if an address has been an authorized signer for an account.
   * @param signer The possibly authorized address.
   * @return Returns `true` if authorized. Returns `false` otherwise.
   */
  function isAuthorizedSigner(address signer) external view returns (bool) {
    return (authorizedBy[signer] != address(0));
  }

  /**
   * @notice Check if an address has not been an authorized signer for an account.
   * @param signer The possibly authorized address.
   * @return Returns `false` if authorized. Returns `true` otherwise.
   */
  function isNotAuthorizedSigner(address signer) internal view returns (bool) {

// Original: contracts/9/specs/harnesses/AccountsHarness.sol:8-35 (relevant _getAuthorizedBy)
  function _getAuthorizedBy(address signer) public view returns (address) {
    return authorizedBy[signer];
  }

  function _getDataEncryptionKeyLen(address a) public view returns (uint256) {
    return this.getDataEncryptionKey(a).length;
  }

  function _getNameLen(address a) public view returns (uint256) {
    return bytes(this.getName(a)).length;
  }

  function _getVoteSigner(address account) public view returns (address) {
    return accounts[account].signers.vote;
  }

  function _getValidatorSigner(address account) public view returns (address) {
    return accounts[account].signers.validator;
  }

  function _getAttestationSigner(address account) public view returns (address) {
    return accounts[account].signers.attestation;
  }

  function _getDefaultSigner(address account, bytes32 role) public view returns (address) {
    return defaultSigners[account][role];
  }


// Original: contracts/9/specs/harnesses/AccountsHarness.sol:32-59 (relevant _getDefaultSigner)
  function _getDefaultSigner(address account, bytes32 role) public view returns (address) {
    return defaultSigners[account][role];
  }

  function isCompletedSignerAuthorization(address account, bytes32 role, address signer)
    public
    view
    returns (bool)
  {
    return signerAuthorizations[account][role][signer].completed;
  }

  function isStartedSignerAuthorization(address account, bytes32 role, address signer)
    public
    view
    returns (bool)
  {
    return signerAuthorizations[account][role][signer].started;
  }

  function _getValidatorRole() public view returns (bytes32) {
    return ValidatorSigner;
  }
  function _getVoteRole() public view returns (bytes32) {
    return VoteSigner;
  }
  function _getAttestationRole() public view returns (bytes32) {
    return AttestationSigner;
