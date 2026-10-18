// Original: contracts/9/contracts/common/Accounts.sol:198-225 (relevant createAccount)
  function createAccount() public returns (bool) {
    require(
      isNotAccount(msg.sender) && isNotAuthorizedSigner(msg.sender),
      "Account already exists or address is an authorized signer for another account"
    );
    Account storage account = accounts[msg.sender];
    account.exists = true;
    emit AccountCreated(msg.sender);
    return true;
  }

  /**
   * @notice Setter for the name of an account.
   * @param name The name to set.
   */
  function setName(string memory name) public {
    require(isAccount(msg.sender), "Register with createAccount to set account name");
    Account storage account = accounts[msg.sender];
    account.name = name;
    emit AccountNameSet(msg.sender, name);
  }

  /**
   * @notice Setter for the wallet address for an account
   * @param walletAddress The wallet address to set for the account
   * @param v The recovery id of the incoming ECDSA signature.
   * @param r Output value r of the ECDSA signature.
   * @param s Output value s of the ECDSA signature.

// Original: contracts/9/contracts/common/Accounts.sol:178-205 (relevant setAccount)
  function setAccount(
    string calldata name,
    bytes calldata dataEncryptionKey,
    address walletAddress,
    uint8 v,
    bytes32 r,
    bytes32 s
  ) external {
    if (!isAccount(msg.sender)) {
      createAccount();
    }
    setName(name);
    setAccountDataEncryptionKey(dataEncryptionKey);
    setWalletAddress(walletAddress, v, r, s);
  }

  /**
   * @notice Creates an account.
   * @return True if account creation succeeded.
   */
  function createAccount() public returns (bool) {
    require(
      isNotAccount(msg.sender) && isNotAuthorizedSigner(msg.sender),
      "Account already exists or address is an authorized signer for another account"
    );
    Account storage account = accounts[msg.sender];
    account.exists = true;
    emit AccountCreated(msg.sender);

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
