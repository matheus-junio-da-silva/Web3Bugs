// Project 6 - Aave Static aToken
// Solidity context for property: getClaimableRewards_stable_after_withdraw
// Literal excerpts from the supplied PropertyGPT Solidity snapshot.
// Context only: historical verification harness/linked contracts are missing.
// StaticATokenLM.sol matches upstream commit 13a004738c533f11710400c1757b9570ef1e0466,
// while the final report states latest reviewed commit ac92951.

// ===== StaticATokenLM.sol =====
// Original source: contracts/6/StaticATokenLM.sol:340-360
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

// Original source: contracts/6/StaticATokenLM.sol:443-478
  function withdraw(
    uint256 assets,
    address receiver,
    address owner
  ) public virtual returns (uint256) {
    require(assets <= maxWithdraw(owner), 'ERC4626: withdraw more than max');

    (uint256 shares, ) = _withdraw(owner, receiver, 0, assets, false);

    return shares;
  }

  ///@inheritdoc IERC4626
  function redeem(
    uint256 shares,
    address receiver,
    address owner
  ) public virtual returns (uint256) {
    require(shares <= maxRedeem(owner), 'ERC4626: redeem more than max');

    (, uint256 assets) = _withdraw(owner, receiver, shares, 0, false);

    return assets;
  }

  ///@inheritdoc IStaticATokenLM
  function redeem(
    uint256 shares,
    address receiver,
    address owner,
    bool toUnderlying
  ) public virtual returns (uint256, uint256) {
    require(shares <= maxRedeem(owner), 'ERC4626: redeem more than max');

    return _withdraw(owner, receiver, shares, 0, toUnderlying);
  }

// Original source: contracts/6/StaticATokenLM.sol:510-554
  function _withdraw(
    address owner,
    address recipient,
    uint256 staticAmount,
    uint256 dynamicAmount,
    bool toUnderlying
  ) internal returns (uint256, uint256) {
    require(recipient != address(0), StaticATokenErrors.INVALID_RECIPIENT);
    require(
      staticAmount == 0 || dynamicAmount == 0,
      StaticATokenErrors.ONLY_ONE_AMOUNT_FORMAT_ALLOWED
    );
    require(
      staticAmount != dynamicAmount,
      StaticATokenErrors.INVALID_ZERO_AMOUNT
    );

    uint256 amountToWithdraw = dynamicAmount;
    uint256 shares = staticAmount;

    if (staticAmount > 0) {
      amountToWithdraw = previewRedeem(staticAmount);
    } else {
      shares = previewWithdraw(dynamicAmount);
    }

    if (msg.sender != owner) {
      uint256 allowed = allowance[owner][msg.sender]; // Saves gas for limited approvals.

      if (allowed != type(uint256).max)
        allowance[owner][msg.sender] = allowed - shares;
    }

    _burn(owner, shares);

    emit Withdraw(msg.sender, recipient, owner, amountToWithdraw, shares);

    if (toUnderlying) {
      POOL.withdraw(_aTokenUnderlying, amountToWithdraw, recipient);
    } else {
      _aToken.safeTransfer(recipient, amountToWithdraw);
    }

    return (shares, amountToWithdraw);
  }

// Original source: contracts/6/StaticATokenLM.sol:562-699
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

  /**
   * @notice Claim rewards on behalf of a user and send them to a receiver
   * @param onBehalfOf The address to claim on behalf of
   * @param rewards The addresses of the rewards
   * @param receiver The address to receive the rewards
   */
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
