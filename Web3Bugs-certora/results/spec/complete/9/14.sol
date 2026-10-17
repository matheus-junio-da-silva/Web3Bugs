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

