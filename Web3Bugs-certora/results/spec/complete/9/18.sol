// Original: contracts/9/contracts/common/Accounts.sol:407-434 (relevant authorizeSignerWithSignature)
  function authorizeSignerWithSignature(address signer, bytes32 role, uint8 v, bytes32 r, bytes32 s)
    public
  {
    authorizeAddressWithRole(signer, role, v, r, s);
    signerAuthorizations[msg.sender][role][signer] = SignerAuthorization({
      started: true,
      completed: true
    });

    emit SignerAuthorized(msg.sender, signer, role);
  }

  function legacyAuthorizeSignerWithSignature(
    address signer,
    bytes32 role,
    uint8 v,
    bytes32 r,
    bytes32 s
  ) private {
    authorizeAddress(signer, v, r, s);
    signerAuthorizations[msg.sender][role][signer] = SignerAuthorization({
      started: true,
      completed: true
    });

    emit SignerAuthorized(msg.sender, signer, role);
  }


// Original: contracts/9/contracts/common/Accounts.sol:538-565 (relevant authorizeAttestationSigner)
  function authorizeAttestationSigner(address signer, uint8 v, bytes32 r, bytes32 s) public {
    legacyAuthorizeSignerWithSignature(signer, AttestationSigner, v, r, s);
    setIndexedSigner(signer, AttestationSigner);

    emit AttestationSignerAuthorized(msg.sender, signer);
  }

  /**
   * @notice Begin the process of authorizing an address to sign on behalf of the account
   * @param signer The address of the signing key to authorize.
   * @param role The role to authorize signing for.
   */
  function authorizeSigner(address signer, bytes32 role) public {
    require(isAccount(msg.sender), "Must first register sender with Account.createAccount");
    require(
      isNotAccount(signer) && isNotAuthorizedSignerForAnotherAccount(msg.sender, signer),
      "Cannot re-authorize address signer"
    );

    signerAuthorizations[msg.sender][role][signer] = SignerAuthorization({
      started: true,
      completed: false
    });
    emit SignerAuthorizationStarted(msg.sender, signer, role);
  }

  /**
   * @notice Finish the process of authorizing an address to sign on behalf of the account.

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

// Original: contracts/9/contracts/common/Accounts.sol:511-538 (relevant authorizeValidatorSignerWithKeys)
  function authorizeValidatorSignerWithKeys(
    address signer,
    uint8 v,
    bytes32 r,
    bytes32 s,
    bytes calldata ecdsaPublicKey,
    bytes calldata blsPublicKey,
    bytes calldata blsPop
  ) external nonReentrant {
    legacyAuthorizeSignerWithSignature(signer, ValidatorSigner, v, r, s);
    setIndexedSigner(signer, ValidatorSigner);

    require(
      getValidators().updatePublicKeys(msg.sender, signer, ecdsaPublicKey, blsPublicKey, blsPop),
      "Failed to update validator keys"
    );
    emit ValidatorSignerAuthorized(msg.sender, signer);
  }

  /**
   * @notice Authorizes an address to sign attestations on behalf of the account.
   * @param signer The address of the signing key to authorize.
   * @param v The recovery id of the incoming ECDSA signature.
   * @param r Output value r of the ECDSA signature.
   * @param s Output value s of the ECDSA signature.
   * @dev v, r, s constitute `signer`'s signature on `msg.sender`.
   */
  function authorizeAttestationSigner(address signer, uint8 v, bytes32 r, bytes32 s) public {
