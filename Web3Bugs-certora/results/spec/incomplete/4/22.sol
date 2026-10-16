// Relevant excerpts for lowerBoundNotZero.
// Target Contract: StakedAaveV3Harness

// Source: contracts/4/contracts/StakedTokenV3.sol
// Original lines: 34-45;76-101

  uint216 public constant INITIAL_EXCHANGE_RATE = 1e18;
  uint256 public constant EXCHANGE_RATE_UNIT = 1e18;

  /// @notice lower bound to prevent spam & avoid exchangeRate issues
  // as returnFunds can be called permissionless an attacker could spam returnFunds(1) to produce exchangeRate snapshots making voting expensive
  uint256 public immutable LOWER_BOUND;

  // Reserved storage space to allow for layout changes in the future.
  uint256[8] private ______gap;
  /// @notice Seconds between starting cooldown and being able to withdraw
  uint256 internal _cooldownSeconds;
  /// @notice The maximum amount of funds that can be slashed at any given time
  constructor(
    IERC20 stakedToken,
    IERC20 rewardToken,
    uint256 unstakeWindow,
    address rewardsVault,
    address emissionManager,
    uint128 distributionDuration
  )
    StakedTokenV2(
      stakedToken,
      rewardToken,
      unstakeWindow,
      rewardsVault,
      emissionManager,
      distributionDuration
    )
  {
    // brick initialize
    lastInitializedRevision = REVISION();
    uint256 decimals = IERC20Metadata(address(stakedToken)).decimals();
    LOWER_BOUND = 10**decimals;
  }

  /**
   * @dev returns the revision of the implementation contract
   * @return The revision
