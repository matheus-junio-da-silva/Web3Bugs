// Project 6 - Aave Static aToken
// Solidity context for property: getClaimableRewards_stable_after_atoken_transferFrom_1
// Literal excerpts from the supplied PropertyGPT Solidity snapshot.
// Context only: historical verification harness/linked contracts are missing.
// StaticATokenLM.sol matches upstream commit 13a004738c533f11710400c1757b9570ef1e0466,
// while the final report states latest reviewed commit ac92951.

// ===== StaticATokenLM.sol =====
// Original source: contracts/6/StaticATokenLM.sol:55-60
  IERC20 internal _aToken;
  address internal _aTokenUnderlying;
  address[] internal _rewardTokens;
  mapping(address => uint256) internal _startIndex;
  mapping(address => mapping(address => UserRewardsData))
    internal _userRewardsData;

// Original source: contracts/6/StaticATokenLM.sol:304-360
  function getCurrentRewardsIndex(address reward)
    public
    view
    returns (uint256)
  {
    if (address(reward) == address(0)) {
      return 0;
    }
    (, uint256 nextIndex) = INCENTIVES_CONTROLLER.getAssetIndex(
      address(_aToken),
      reward
    );
    return nextIndex;
  }

  ///@inheritdoc IStaticATokenLM
  function getTotalClaimableRewards(address reward)
    external
    view
    returns (uint256)
  {
    if (reward == address(0)) {
      return 0;
    }

    address[] memory assets = new address[](1);
    assets[0] = address(_aToken);
    uint256 freshRewards = INCENTIVES_CONTROLLER.getUserRewards(
      assets,
      address(this),
      reward
    );
    return IERC20(reward).balanceOf(address(this)) + freshRewards;
  }

  ///@inheritdoc IStaticATokenLM
  function getClaimableRewards(address user, address reward)
    external
    view
    returns (uint256)
  {
    return
      _getClaimableRewards(
        user,
        reward,
        balanceOf[user],
        getCurrentRewardsIndex(reward)
      );
  }

  ///@inheritdoc IStaticATokenLM
  function getUnclaimedRewards(address user, address reward)
    external
    view
    returns (uint256)
  {
    return _userRewardsData[user][reward].unclaimedRewards;

// Original source: contracts/6/StaticATokenLM.sol:562-653
  function _beforeTokenTransfer(
    address from,
    address to,
    uint256 amount
  ) internal override {
    for (uint256 i = 0; i < _rewardTokens.length; i++) {
      address rewardToken = address(_rewardTokens[i]);
      uint256 rewardsIndex = getCurrentRewardsIndex(rewardToken);
      if (from != address(0)) {
        _updateUser(from, rewardsIndex, rewardToken);
      }
      if (to != address(0) && from != to) {
        _updateUser(to, rewardsIndex, rewardToken);
      }
    }
  }

  /**
   * @notice Adding the pending rewards to the unclaimed for specific user and updating user index
   * @param user The address of the user to update
   * @param currentRewardsIndex The current rewardIndex
   * @param rewardToken The address of the reward token
   */
  function _updateUser(
    address user,
    uint256 currentRewardsIndex,
    address rewardToken
  ) internal {
    uint256 balance = balanceOf[user];
    if (balance > 0) {
      _userRewardsData[user][rewardToken]
        .unclaimedRewards = _getClaimableRewards(
        user,
        rewardToken,
        balance,
        currentRewardsIndex
      ).toUint128();
    }
    _userRewardsData[user][rewardToken]
      .rewardsIndexOnLastInteraction = currentRewardsIndex.toUint128();
  }

  /**
   * @notice Compute the pending in WAD. Pending is the amount to add (not yet unclaimed) rewards in WAD.
   * @param balance The balance of the user
   * @param rewardsIndexOnLastInteraction The index which was on the last interaction of the user
   * @param currentRewardsIndex The current rewards index in the system
   * @param assetUnit One unit of asset (10**decimals)
   * @return The amount of pending rewards in WAD
   */
  function _getPendingRewards(
    uint256 balance,
    uint256 rewardsIndexOnLastInteraction,
    uint256 currentRewardsIndex,
    uint256 assetUnit
  ) internal pure returns (uint256) {
    if (balance == 0) {
      return 0;
    }
    return
      (balance * (currentRewardsIndex - rewardsIndexOnLastInteraction)) /
      assetUnit;
  }

  /**
   * @notice Compute the claimable rewards for a user
   * @param user The address of the user
   * @param reward The address of the reward
   * @param balance The balance of the user in WAD
   * @return The total rewards that can be claimed by the user (if `fresh` flag true, after updating rewards)
   */
  function _getClaimableRewards(
    address user,
    address reward,
    uint256 balance,
    uint256 currentRewardsIndex
  ) internal view returns (uint256) {
    UserRewardsData memory currentUserRewardsData = _userRewardsData[user][
      reward
    ];
    uint256 assetUnit = 10**decimals;
    return
      currentUserRewardsData.unclaimedRewards +
      _getPendingRewards(
        balance,
        currentUserRewardsData.rewardsIndexOnLastInteraction == 0
          ? _startIndex[reward]
          : currentUserRewardsData.rewardsIndexOnLastInteraction,
        currentRewardsIndex,
        assetUnit
      );
  }
