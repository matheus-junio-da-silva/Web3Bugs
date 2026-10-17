// Original: contracts/9/contracts/common/Accounts.sol:805-832 (relevant isLegacyRole)
  function isLegacyRole(bytes32 role) public pure returns (bool) {
    return role == VoteSigner || role == ValidatorSigner || role == AttestationSigner;
  }

  /**
   * @notice Returns the legacy signer for the specified account and
   * role. If no signer has been specified it will return the account itself.
   * @param _account The address of the account.
   * @param role The role of the signer.
   */
  function getLegacySigner(address _account, bytes32 role) public view returns (address) {
    require(isLegacyRole(role), "Role is not a legacy signer");

    Account storage account = accounts[_account];
    address signer;
    if (role == ValidatorSigner) {
      signer = account.signers.validator;
    } else if (role == AttestationSigner) {
      signer = account.signers.attestation;
    } else if (role == VoteSigner) {
      signer = account.signers.vote;
    }

    return signer == address(0) ? _account : signer;
  }

  /**
   * @notice Returns the default signer for the specified account and

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


// Original: contracts/9/specs/harnesses/AccountsHarness.sol:36-62 (relevant isCompletedSignerAuthorization)
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
  }
}


// Original: contracts/9/specs/harnesses/AccountsHarness.sol:44-62 (relevant isStartedSignerAuthorization)
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
  }
}

