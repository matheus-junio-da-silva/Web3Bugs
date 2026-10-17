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

// Original: contracts/9/contracts/common/Accounts.sol:848-875 (relevant getIndexedSigner)
  function getIndexedSigner(address account, bytes32 role) public view returns (address) {
    return isLegacyRole(role) ? getLegacySigner(account, role) : getDefaultSigner(account, role);
  }

  /**
   * @notice Returns the vote signer for the specified account.
   * @param account The address of the account.
   * @return The address with which the account can sign votes.
   */
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

// Original: contracts/9/contracts/common/Accounts.sol:837-864 (relevant getDefaultSigner)
  function getDefaultSigner(address account, bytes32 role) public view returns (address) {
    address defaultSigner = defaultSigners[account][role];
    return defaultSigner == address(0) ? account : defaultSigner;
  }

  /**
   * @notice Returns the indexed signer for the specified account and role.
   * If no signer has been specified it will return the account itself.
   * @param account The address of the account.
   * @param role The role of the signer.
   */
  function getIndexedSigner(address account, bytes32 role) public view returns (address) {
    return isLegacyRole(role) ? getLegacySigner(account, role) : getDefaultSigner(account, role);
  }

  /**
   * @notice Returns the vote signer for the specified account.
   * @param account The address of the account.
   * @return The address with which the account can sign votes.
   */
  function getVoteSigner(address account) public view returns (address) {
    return getLegacySigner(account, VoteSigner);
  }

  /**
   * @notice Returns the validator signer for the specified account.
   * @param account The address of the account.
   * @return The address with which the account can register a validator or group.

// Original: contracts/9/contracts/common/Accounts.sol:815-842 (relevant getLegacySigner)
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
   * role. If no signer has been specified it will return the account itself.
   * @param account The address of the account.
   * @param role The role of the signer.
   */
  function getDefaultSigner(address account, bytes32 role) public view returns (address) {
    address defaultSigner = defaultSigners[account][role];
    return defaultSigner == address(0) ? account : defaultSigner;
  }

  /**
