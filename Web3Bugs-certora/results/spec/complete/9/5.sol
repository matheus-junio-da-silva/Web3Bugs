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

// Original: contracts/9/contracts/common/Accounts.sol:461-488 (relevant authorizeValidatorSigner)
  function authorizeValidatorSigner(address signer, uint8 v, bytes32 r, bytes32 s)
    external
    nonReentrant
  {
    legacyAuthorizeSignerWithSignature(signer, ValidatorSigner, v, r, s);
    setIndexedSigner(signer, ValidatorSigner);

    require(!getValidators().isValidator(msg.sender), "Cannot authorize validator signer");
    emit ValidatorSignerAuthorized(msg.sender, signer);
  }

  /**
   * @notice Authorizes an address to sign consensus messages on behalf of the account.
   * @param signer The address of the signing key to authorize.
   * @param v The recovery id of the incoming ECDSA signature.
   * @param r Output value r of the ECDSA signature.
   * @param s Output value s of the ECDSA signature.
   * @param ecdsaPublicKey The ECDSA public key corresponding to `signer`.
   * @dev v, r, s constitute `signer`'s signature on `msg.sender`.
   */
  function authorizeValidatorSignerWithPublicKey(
    address signer,
    uint8 v,
    bytes32 r,
    bytes32 s,
    bytes calldata ecdsaPublicKey
  ) external nonReentrant {
    legacyAuthorizeSignerWithSignature(signer, ValidatorSigner, v, r, s);

// Original: contracts/9/contracts/common/Accounts.sol:443-470 (relevant authorizeVoteSigner)
  function authorizeVoteSigner(address signer, uint8 v, bytes32 r, bytes32 s)
    external
    nonReentrant
  {
    legacyAuthorizeSignerWithSignature(signer, VoteSigner, v, r, s);
    setIndexedSigner(signer, VoteSigner);

    emit VoteSignerAuthorized(msg.sender, signer);
  }

  /**
   * @notice Authorizes an address to sign consensus messages on behalf of the account.
   * @param signer The address of the signing key to authorize.
   * @param v The recovery id of the incoming ECDSA signature.
   * @param r Output value r of the ECDSA signature.
   * @param s Output value s of the ECDSA signature.
   * @dev v, r, s constitute `signer`'s signature on `msg.sender`.
   */
  function authorizeValidatorSigner(address signer, uint8 v, bytes32 r, bytes32 s)
    external
    nonReentrant
  {
    legacyAuthorizeSignerWithSignature(signer, ValidatorSigner, v, r, s);
    setIndexedSigner(signer, ValidatorSigner);

    require(!getValidators().isValidator(msg.sender), "Cannot authorize validator signer");
    emit ValidatorSignerAuthorized(msg.sender, signer);
  }

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

