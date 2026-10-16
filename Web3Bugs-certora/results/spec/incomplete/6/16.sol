// Project 6 - Aave Static aToken
// Solidity context for property: getClaimableRewards_stable_SANITY
// Literal excerpts from the supplied PropertyGPT Solidity snapshot.
// Context only: historical verification harness/linked contracts are missing.
// StaticATokenLM.sol matches upstream commit 13a004738c533f11710400c1757b9570ef1e0466,
// while the final report states latest reviewed commit ac92951.

// ===== StaticATokenLM.sol =====
// Original source: contracts/6/StaticATokenLM.sol:280-360
  function claimRewardsOnBehalf(
    address onBehalfOf,
    address receiver,
    address[] memory rewards
  ) external {
    require(
      msg.sender == onBehalfOf ||
        msg.sender == INCENTIVES_CONTROLLER.getClaimer(onBehalfOf),
      StaticATokenErrors.INVALID_CLAIMER
    );
    _claimRewardsOnBehalf(onBehalfOf, receiver, rewards);
  }

  ///@inheritdoc IStaticATokenLM
  function claimRewards(address receiver, address[] memory rewards) external {
    _claimRewardsOnBehalf(msg.sender, receiver, rewards);
  }

  ///@inheritdoc IStaticATokenLM
  function claimRewardsToSelf(address[] memory rewards) external {
    _claimRewardsOnBehalf(msg.sender, msg.sender, rewards);
  }

  ///@inheritdoc IStaticATokenLM
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

// Original source: contracts/6/StaticATokenLM.sol:661-699
  function _claimRewardsOnBehalf(
    address onBehalfOf,
    address receiver,
    address[] memory rewards
  ) internal {
    for (uint256 i = 0; i < rewards.length; i++) {
      if (address(rewards[i]) == address(0)) {
        return;
      }
      uint256 currentRewardsIndex = getCurrentRewardsIndex(rewards[i]);
      uint256 balance = balanceOf[onBehalfOf];
      uint256 userReward = _getClaimableRewards(
        onBehalfOf,
        rewards[i],
        balance,
        currentRewardsIndex
      );
      uint256 totalRewardTokenBalance = IERC20(rewards[i]).balanceOf(
        address(this)
      );
      uint256 unclaimedReward = 0;

      if (userReward > totalRewardTokenBalance) {
        totalRewardTokenBalance += collectAndUpdateRewards(address(rewards[i]));
      }

      if (userReward > totalRewardTokenBalance) {
        unclaimedReward = userReward - totalRewardTokenBalance;
        userReward = totalRewardTokenBalance;
      }
      if (userReward > 0) {
        _userRewardsData[onBehalfOf][rewards[i]]
          .unclaimedRewards = unclaimedReward.toUint128();
        _userRewardsData[onBehalfOf][rewards[i]]
          .rewardsIndexOnLastInteraction = currentRewardsIndex.toUint128();
        IERC20(rewards[i]).safeTransfer(receiver, userReward);
      }
    }
  }
