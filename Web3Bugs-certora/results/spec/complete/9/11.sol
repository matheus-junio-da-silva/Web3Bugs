// Original: contracts/9/contracts/common/Accounts.sol:908-935 (relevant hasAuthorizedSigner)
  function hasAuthorizedSigner(address account, string calldata role) external view returns (bool) {
    return hasIndexedSigner(account, keccak256(abi.encodePacked(role)));
  }

  /**
   * @notice Returns if account has specified a dedicated vote signer.
   * @param account The address of the account.
   * @return Whether the account has specified a dedicated vote signer.
   */
  function hasAuthorizedVoteSigner(address account) external view returns (bool) {
    return hasLegacySigner(account, VoteSigner);
  }

  /**
   * @notice Returns if account has specified a dedicated validator signer.
   * @param account The address of the account.
   * @return Whether the account has specified a dedicated validator signer.
   */
  function hasAuthorizedValidatorSigner(address account) external view returns (bool) {
    return hasLegacySigner(account, ValidatorSigner);
  }

  /**
   * @notice Returns if account has specified a dedicated attestation signer.
   * @param account The address of the account.
   * @return Whether the account has specified a dedicated attestation signer.
   */
  function hasAuthorizedAttestationSigner(address account) external view returns (bool) {

// Original: contracts/9/contracts/common/Accounts.sol:963-990 (relevant batchGetMetadataURL)
  function batchGetMetadataURL(address[] calldata accountsToQuery)
    external
    view
    returns (uint256[] memory, bytes memory)
  {
    uint256 totalSize = 0;
    uint256[] memory sizes = new uint256[](accountsToQuery.length);
    for (uint256 i = 0; i < accountsToQuery.length; i = i.add(1)) {
      sizes[i] = bytes(accounts[accountsToQuery[i]].metadataURL).length;
      totalSize = totalSize.add(sizes[i]);
    }

    bytes memory data = new bytes(totalSize);
    uint256 pointer = 0;
    for (uint256 i = 0; i < accountsToQuery.length; i = i.add(1)) {
      for (uint256 j = 0; j < sizes[i]; j = j.add(1)) {
        data[pointer] = bytes(accounts[accountsToQuery[i]].metadataURL)[j];
        pointer = pointer.add(1);
      }
    }
    return (sizes, data);
  }

  /**
   * @notice Getter for the data encryption key and version.
   * @param account The address of the account to get the key for
   * @return dataEncryptionKey secp256k1 public key for data encryption. Preferably compressed.
   */

// Original: contracts/9/contracts/common/Accounts.sol:299-326 (relevant getOffchainStorageRoots)
  function getOffchainStorageRoots(address account)
    external
    view
    returns (bytes memory, uint256[] memory)
  {
    require(isAccount(account), "Unknown account");
    uint256 numberRoots = offchainStorageRoots[account].length;
    uint256 totalLength = 0;
    for (uint256 i = 0; i < numberRoots; i++) {
      totalLength = totalLength.add(offchainStorageRoots[account][i].length);
    }

    bytes memory concatenated = new bytes(totalLength);
    uint256 lastIndex = 0;
    uint256[] memory lengths = new uint256[](numberRoots);
    for (uint256 i = 0; i < numberRoots; i++) {
      bytes storage root = offchainStorageRoots[account][i];
      lengths[i] = root.length;
      for (uint256 j = 0; j < lengths[i]; j++) {
        concatenated[lastIndex] = root[j];
        lastIndex++;
      }
    }

    return (concatenated, lengths);
  }

  /**

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
