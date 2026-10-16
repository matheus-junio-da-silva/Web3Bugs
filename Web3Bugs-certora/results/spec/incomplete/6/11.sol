// Project 6 - Aave Static aToken
// Solidity context for property: reward_balance_stable_after_collectAndUpdateRewards
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

// Original source: contracts/6/StaticATokenLM.sol:262-277
  function collectAndUpdateRewards(address reward) public returns (uint256) {
    if (reward == address(0)) {
      return 0;
    }

    address[] memory assets = new address[](1);
    assets[0] = address(_aToken);

    return
      INCENTIVES_CONTROLLER.claimRewards(
        assets,
        type(uint256).max,
        address(this),
        reward
      );
  }

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
