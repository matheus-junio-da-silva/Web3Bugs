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
