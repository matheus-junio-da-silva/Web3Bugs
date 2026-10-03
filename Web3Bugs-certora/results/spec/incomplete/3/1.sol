// Relevant excerpts for LendIsBackedByAave.
// Source: contracts/3/contracts/LendToAaveMigrator.sol
// Original lines: 12-18;40-46;57-79;94-104

contract LendToAaveMigrator is VersionedInitializable {
    IERC20 public immutable AAVE;
    IERC20 public immutable LEND;
    uint256 public immutable LEND_AAVE_RATIO;
    uint256 public constant REVISION = 2;
    
    uint256 public _totalLendMigrated;
    constructor(IERC20 aave, IERC20 lend, uint256 lendAaveRatio) public {
        AAVE = aave;
        LEND = lend;
        LEND_AAVE_RATIO = lendAaveRatio;

        lastInitializedRevision = REVISION;
    }
    function initialize(address aaveMerkleDistributor, uint256 lendToMigratorAmount, uint256 lendToLendAmount, uint256 lendToAaveAmount) public initializer {
        uint256 lendAmount = lendToMigratorAmount + lendToLendAmount + lendToAaveAmount;
        uint256 migratorLendBalance = _totalLendMigrated + lendToMigratorAmount;

        // account for the LEND sent to the contract for the total migration
        _totalLendMigrated += lendAmount;

        // transfer AAVE + LEND sent to this contract
        uint256 amountToRescue = lendAmount / LEND_AAVE_RATIO;
        AAVE.transfer(aaveMerkleDistributor, amountToRescue);

        LEND.transfer(address(LEND), migratorLendBalance);

        emit LendMigrated(address(this), lendAmount);
        emit AaveTokensRescued(address(this), aaveMerkleDistributor, amountToRescue);

        // checks that the amount of AAVE not migrated is less or equal as the amount of AAVE disposable for migration
        // we have found that there was a previous small surplus on the AAVE token amount found on the LendToAaveMigrator
        // contract previous to the rescue, that is why we need to use <= instead of == . This amount is 582968318731898974 (0,58 AAVE)
        require((LEND.totalSupply() - LEND.balanceOf(address(LEND)) - lendToAaveAmount ) / LEND_AAVE_RATIO <= AAVE.balanceOf(address(this)),
            'INCORRECT_BALANCE_RESCUED'
        );
    }
    function migrateFromLEND(uint256 amount) external {
        require(lastInitializedRevision != 0, "MIGRATION_NOT_STARTED");

        _totalLendMigrated = _totalLendMigrated + amount;
        LEND.transferFrom(msg.sender, address(this), amount);
        AAVE.transfer(msg.sender, amount / LEND_AAVE_RATIO);

        LEND.transfer(address(LEND), amount);
        
        emit LendMigrated(msg.sender, amount);
    }
