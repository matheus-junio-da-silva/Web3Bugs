// Historical Solidity: contracts/21/0.8.9/DepositSecurityModule.sol lines 75-90
    uint256 internal maxDepositsPerBlock;
    uint256 internal minDepositBlockDistance;
    uint256 internal pauseIntentValidityPeriodBlocks;

    address internal owner;

    uint256 internal quorum;
    address[] internal guardians;
    mapping(address => uint256) internal guardianIndicesOneBased; // 1-based

    constructor(
        address _lido,
        address _depositContract,
        address _stakingRouter,
        uint256 _maxDepositsPerBlock,
        uint256 _minDepositBlockDistance,

// Historical Solidity: contracts/21/0.8.9/DepositSecurityModule.sol lines 109-119

        PAUSE_MESSAGE_PREFIX = keccak256(
            abi.encodePacked(
                // keccak256("lido.DepositSecurityModule.PAUSE_MESSAGE")
                bytes32(0x9c4c40205558f12027f21204d6218b8006985b7a6359bcab15404bcc3e3fa122),
                block.chainid,
                address(this)
            )
        );

        _setOwner(msg.sender);

// Historical Solidity: contracts/21/0.8.9/DepositSecurityModule.sol lines 211-235
    /**
     * Returns number of valid guardian signatures required to vet (depositRoot, nonce) pair.
     */
    function getGuardianQuorum() external view returns (uint256) {
        return quorum;
    }

    function setGuardianQuorum(uint256 newValue) external onlyOwner {
        _setGuardianQuorum(newValue);
    }

    function _setGuardianQuorum(uint256 newValue) internal {
        // we're intentionally allowing setting quorum value higher than the number of guardians
        if (quorum != newValue) {
            quorum = newValue;
            emit GuardianQuorumChanged(newValue);
        }
    }

    /**
     * Returns guardian committee member list.
     */
    function getGuardians() external view returns (address[] memory) {
        return guardians;
    }

// Historical Solidity: contracts/21/0.8.9/DepositSecurityModule.sol lines 259-314
    /**
     * Adds a guardian address and sets a new quorum value.
     * Reverts if the address is already a guardian.
     *
     * Only callable by the owner.
     */
    function addGuardian(address addr, uint256 newQuorum) external onlyOwner {
        _addGuardian(addr);
        _setGuardianQuorum(newQuorum);
    }

    /**
     * Adds a set of guardian addresses and sets a new quorum value.
     * Reverts any of them is already a guardian.
     *
     * Only callable by the owner.
     */
    function addGuardians(address[] memory addresses, uint256 newQuorum) external onlyOwner {
        for (uint256 i = 0; i < addresses.length; ++i) {
            _addGuardian(addresses[i]);
        }
        _setGuardianQuorum(newQuorum);
    }

    function _addGuardian(address _newGuardian) internal {
        if (_newGuardian == address(0)) revert ZeroAddress("_newGuardian");
        if (_isGuardian(_newGuardian)) revert DuplicateAddress(_newGuardian);
        guardians.push(_newGuardian);
        guardianIndicesOneBased[_newGuardian] = guardians.length;
        emit GuardianAdded(_newGuardian);
    }

    /**
     * Removes a guardian with the given address and sets a new quorum value.
     *
     * Only callable by the owner.
     */
    function removeGuardian(address addr, uint256 newQuorum) external onlyOwner {
        uint256 indexOneBased = guardianIndicesOneBased[addr];
        if (indexOneBased == 0) revert NotAGuardian(addr);

        uint256 totalGuardians = guardians.length;
        assert(indexOneBased <= totalGuardians);

        if (indexOneBased != totalGuardians) {
            address addrToMove = guardians[totalGuardians - 1];
            guardians[indexOneBased - 1] = addrToMove;
            guardianIndicesOneBased[addrToMove] = indexOneBased;
        }

        guardianIndicesOneBased[addr] = 0;
        guardians.pop();

        _setGuardianQuorum(newQuorum);

        emit GuardianRemoved(addr);
