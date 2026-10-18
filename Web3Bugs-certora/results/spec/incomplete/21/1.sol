// Historical Solidity: contracts/21/0.8.9/DepositSecurityModule.sol lines 7-7
import {ECDSA} from "../common/lib/ECDSA.sol";

// Historical Solidity: contracts/21/0.8.9/DepositSecurityModule.sol lines 34-95
contract DepositSecurityModule {
    /**
     * Short ECDSA signature as defined in https://eips.ethereum.org/EIPS/eip-2098.
     */
    struct Signature {
        bytes32 r;
        bytes32 vs;
    }

    event OwnerChanged(address newValue);
    event PauseIntentValidityPeriodBlocksChanged(uint256 newValue);
    event MaxDepositsChanged(uint256 newValue);
    event MinDepositBlockDistanceChanged(uint256 newValue);
    event GuardianQuorumChanged(uint256 newValue);
    event GuardianAdded(address guardian);
    event GuardianRemoved(address guardian);
    event DepositsPaused(address indexed guardian, uint24 indexed stakingModuleId);
    event DepositsUnpaused(uint24 indexed stakingModuleId);

    error ZeroAddress(string field);
    error DuplicateAddress(address addr);
    error NotAnOwner(address caller);
    error InvalidSignature();
    error SignatureNotSorted();
    error DepositNoQuorum();
    error DepositRootChanged();
    error DepositInactiveModule();
    error DepositTooFrequent();
    error DepositUnexpectedBlockHash();
    error DepositNonceChanged();
    error PauseIntentExpired();
    error NotAGuardian(address addr);
    error ZeroParameter(string parameter);

    bytes32 public immutable ATTEST_MESSAGE_PREFIX;
    bytes32 public immutable PAUSE_MESSAGE_PREFIX;

    ILido public immutable LIDO;
    IStakingRouter public immutable STAKING_ROUTER;
    IDepositContract public immutable DEPOSIT_CONTRACT;

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
        uint256 _pauseIntentValidityPeriodBlocks
    ) {
        if (_lido == address(0)) revert ZeroAddress("_lido");
        if (_depositContract == address(0)) revert ZeroAddress ("_depositContract");
        if (_stakingRouter == address(0)) revert ZeroAddress ("_stakingRouter");

// Historical Solidity: contracts/21/0.8.9/DepositSecurityModule.sol lines 210-235

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

// Historical Solidity: contracts/21/0.8.9/DepositSecurityModule.sol lines 379-395
     */
    function canDeposit(uint256 stakingModuleId) external view returns (bool) {
        if (!STAKING_ROUTER.hasStakingModule(stakingModuleId)) return false;

        bool isModuleActive = STAKING_ROUTER.getStakingModuleIsActive(stakingModuleId);
        uint256 lastDepositBlock = STAKING_ROUTER.getStakingModuleLastDepositBlock(stakingModuleId);
        bool isLidoCanDeposit = LIDO.canDeposit();
        return (
            isModuleActive
            && quorum > 0
            && block.number - lastDepositBlock >= minDepositBlockDistance
            && isLidoCanDeposit
        );
    }

    /**
     * Calls LIDO.deposit(maxDepositsPerBlock, stakingModuleId, depositCalldata).

// Historical Solidity: contracts/21/0.8.9/DepositSecurityModule.sol lines 396-459
     *
     * Reverts if any of the following is true:
     *   1. IDepositContract.get_deposit_root() != depositRoot.
     *   2. StakingModule.getNonce() != nonce.
     *   3. The number of guardian signatures is less than getGuardianQuorum().
     *   4. An invalid or non-guardian signature received.
     *   5. block.number - StakingModule.getLastDepositBlock() < minDepositBlockDistance.
     *   6. blockhash(blockNumber) != blockHash.
     *
     * Signatures must be sorted in ascending order by index of the guardian. Each signature must
     * be produced for keccak256 hash of the following message (each component taking 32 bytes):
     *
     * | ATTEST_MESSAGE_PREFIX | blockNumber | blockHash | depositRoot | stakingModuleId | nonce |
     */
    function depositBufferedEther(
        uint256 blockNumber,
        bytes32 blockHash,
        bytes32 depositRoot,
        uint256 stakingModuleId,
        uint256 nonce,
        bytes calldata depositCalldata,
        Signature[] calldata sortedGuardianSignatures
    ) external {
        if (quorum == 0 || sortedGuardianSignatures.length < quorum) revert DepositNoQuorum();

        bytes32 onchainDepositRoot = IDepositContract(DEPOSIT_CONTRACT).get_deposit_root();
        if (depositRoot != onchainDepositRoot) revert DepositRootChanged();

        if (!STAKING_ROUTER.getStakingModuleIsActive(stakingModuleId)) revert DepositInactiveModule();

        uint256 lastDepositBlock = STAKING_ROUTER.getStakingModuleLastDepositBlock(stakingModuleId);
        if (block.number - lastDepositBlock < minDepositBlockDistance) revert DepositTooFrequent();
        if (blockHash == bytes32(0) || blockhash(blockNumber) != blockHash) revert DepositUnexpectedBlockHash();

        uint256 onchainNonce = STAKING_ROUTER.getStakingModuleNonce(stakingModuleId);
        if (nonce != onchainNonce) revert DepositNonceChanged();

        _verifySignatures(depositRoot, blockNumber, blockHash, stakingModuleId, nonce, sortedGuardianSignatures);

        LIDO.deposit(maxDepositsPerBlock, stakingModuleId, depositCalldata);
    }

    function _verifySignatures(
        bytes32 depositRoot,
        uint256 blockNumber,
        bytes32 blockHash,
        uint256 stakingModuleId,
        uint256 nonce,
        Signature[] memory sigs
    ) internal view {
        bytes32 msgHash = keccak256(
            abi.encodePacked(ATTEST_MESSAGE_PREFIX, blockNumber, blockHash, depositRoot, stakingModuleId, nonce)
        );

        address prevSignerAddr = address(0);

        for (uint256 i = 0; i < sigs.length; ++i) {
            address signerAddr = ECDSA.recover(msgHash, sigs[i].r, sigs[i].vs);
            if (!_isGuardian(signerAddr)) revert InvalidSignature();
            if (signerAddr <= prevSignerAddr) revert SignatureNotSorted();
            prevSignerAddr = signerAddr;
        }
    }
}
