// Original: contracts/23/src/DripsHub.sol lines 159-163
    /// @param erc20 The ERC-20 token
    /// @return balance The balance of the token.
    function totalBalance(IERC20 erc20) public view returns (uint256 balance) {
        return _dripsHubStorage().totalBalances[erc20];
    }

// Original: contracts/23/src/Managed.sol lines 18-22
abstract contract Managed is UUPSUpgradeable {
    /// @notice The pointer to the storage slot with the boolean holding the paused state.
    //bytes32 private immutable pausedSlot = erc1967Slot("eip1967.managed.paused");
    bytes32 public immutable pausedSlot = erc1967Slot("eip1967.managed.paused");

// Original: contracts/23/src/DripsHub.sol lines 60-64
    uint256 public constant MAX_TOTAL_BALANCE = _MAX_TOTAL_DRIPS_BALANCE;
    /// @notice The ERC-1967 storage slot holding a single `DripsHubStorage` structure.
    //bytes32 private immutable _storageSlot = erc1967Slot("eip1967.dripsHub.storage");
    bytes32 public immutable _storageSlot = erc1967Slot("eip1967.dripsHub.storage");
