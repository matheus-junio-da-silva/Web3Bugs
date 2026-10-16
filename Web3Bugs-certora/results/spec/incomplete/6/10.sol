// Project 6 - Aave Static aToken
// Solidity context for property: totalAssets_stable_after_collectAndUpdateRewards
// Literal excerpts from the supplied PropertyGPT Solidity snapshot.
// Context only: historical verification harness/linked contracts are missing.
// StaticATokenLM.sol matches upstream commit 13a004738c533f11710400c1757b9570ef1e0466,
// while the final report states latest reviewed commit ac92951.

// ===== StaticATokenLM.sol =====
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

// Original source: contracts/6/StaticATokenLM.sol:304-337
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

// Original source: contracts/6/StaticATokenLM.sol:384-386
  function totalAssets() external view returns (uint256) {
    return _aToken.balanceOf(address(this));
  }
