// Relevant excerpts for LendIsBackedByAaveIncInitialize.
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

// Source: contracts/3/contracts/AaveTokenV2.sol
// Original lines: 728-734;1124-1126;1171-1181;1236-1266

  function safeTransfer(
    IERC20 token,
    address to,
    uint256 value
  ) internal {
    callOptionalReturn(token, abi.encodeWithSelector(token.transfer.selector, to, value));
  }
contract AaveTokenV2 is GovernancePowerDelegationERC20, VersionedInitializable {
  using SafeMath for uint256;
  using SafeERC20 for IERC20;
  function initialize(address[] memory tokens, uint256[] memory amounts, address aaveMerkleDistributor, address lendToken, uint256 lendToAaveAmount) external initializer {
    // send tokens to distributor
    require(tokens.length == amounts.length, 'initialize(): amounts and tokens lengths inconsistent'); 
    for(uint i = 0; i < tokens.length; i++) {
      IERC20(tokens[i]).safeTransfer(aaveMerkleDistributor, amounts[i]);

      emit TokensRescued(tokens[i], aaveMerkleDistributor, amounts[i]);
    }

    IERC20(lendToken).safeTransfer(lendToken, lendToAaveAmount);
  }
  function _beforeTokenTransfer(
    address from,
    address to,
    uint256 amount
  ) internal override {
    address votingFromDelegatee = _getDelegatee(from, _votingDelegates);
    address votingToDelegatee = _getDelegatee(to, _votingDelegates);

    _moveDelegatesByType(
      votingFromDelegatee,
      votingToDelegatee,
      amount,
      DelegationType.VOTING_POWER
    );

    address propPowerFromDelegatee = _getDelegatee(from, _propositionPowerDelegates);
    address propPowerToDelegatee = _getDelegatee(to, _propositionPowerDelegates);

    _moveDelegatesByType(
      propPowerFromDelegatee,
      propPowerToDelegatee,
      amount,
      DelegationType.PROPOSITION_POWER
    );

    // caching the aave governance address to avoid multiple state loads
    ITransferHook aaveGovernance = _aaveGovernance;
    if (aaveGovernance != ITransferHook(0)) {
      aaveGovernance.onTransfer(from, to, amount);
    }
  }
