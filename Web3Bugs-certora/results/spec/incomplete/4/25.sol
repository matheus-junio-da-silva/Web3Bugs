// Relevant excerpts for totalSupplyGreaterThanUserBalance.
// Target Contract: StakedAaveV3Harness

// Source: contracts/4/contracts/StakedTokenV2.sol
// Original lines: 1-24

// SPDX-License-Identifier: agpl-3.0
pragma solidity ^0.8.0;

import {IERC20} from '../interfaces/IERC20.sol';
import {IStakedTokenV2} from '../interfaces/IStakedTokenV2.sol';

import {ERC20} from '../lib/ERC20.sol';
import {DistributionTypes} from '../lib/DistributionTypes.sol';
import {SafeERC20} from '../lib/SafeERC20.sol';

import {VersionedInitializable} from '../utils/VersionedInitializable.sol';
import {AaveDistributionManager} from './AaveDistributionManager.sol';
import {GovernancePowerWithSnapshot} from '../lib/GovernancePowerWithSnapshot.sol';

/**
 * @title StakedTokenV2
 * @notice Contract to stake Aave token, tokenize the position and get rewards, inheriting from a distribution manager contract
 * @author BGD Labs
 */
abstract contract StakedTokenV2 is
  IStakedTokenV2,
  GovernancePowerWithSnapshot,
  VersionedInitializable,
  AaveDistributionManager

// Source: contracts/4/contracts/StakedTokenV3.sol
// Original lines: 442-474;479-527;555-581

  function _stake(
    address from,
    address to,
    uint256 amount
  ) internal {
    require(!inPostSlashingPeriod, 'SLASHING_ONGOING');
    require(amount != 0, 'INVALID_ZERO_AMOUNT');

    uint256 balanceOfTo = balanceOf(to);

    uint256 accruedRewards = _updateUserAssetInternal(
      to,
      address(this),
      balanceOfTo,
      totalSupply()
    );

    if (accruedRewards != 0) {
      stakerRewardsToClaim[to] = stakerRewardsToClaim[to] + accruedRewards;
      emit RewardsAccrued(to, accruedRewards);
    }

    uint256 sharesToMint = previewStake(amount);

    STAKED_TOKEN.safeTransferFrom(from, address(this), amount);

    _mint(to, sharesToMint);

    emit Staked(from, to, amount, sharesToMint);
  }

  /**
   * @dev Redeems staked tokens, and stop earning rewards
  function _redeem(
    address from,
    address to,
    uint256 amount
  ) internal {
    require(amount != 0, 'INVALID_ZERO_AMOUNT');

    CooldownSnapshot memory cooldownSnapshot = stakersCooldowns[from];
    if (!inPostSlashingPeriod) {
      require(
        (block.timestamp >= cooldownSnapshot.timestamp + _cooldownSeconds),
        'INSUFFICIENT_COOLDOWN'
      );
      require(
        (block.timestamp - (cooldownSnapshot.timestamp + _cooldownSeconds) <=
          UNSTAKE_WINDOW),
        'UNSTAKE_WINDOW_FINISHED'
      );
    }

    uint256 balanceOfFrom = balanceOf(from);
    uint256 maxRedeemable = inPostSlashingPeriod
      ? balanceOfFrom
      : cooldownSnapshot.amount;
    require(maxRedeemable != 0, 'INVALID_ZERO_MAX_REDEEMABLE');

    uint256 amountToRedeem = (amount > maxRedeemable) ? maxRedeemable : amount;

    _updateCurrentUnclaimedRewards(from, balanceOfFrom, true);

    uint256 underlyingToRedeem = previewRedeem(amountToRedeem);

    _burn(from, amountToRedeem);

    if (cooldownSnapshot.timestamp != 0) {
      if (cooldownSnapshot.amount - amountToRedeem == 0) {
        delete stakersCooldowns[from];
      } else {
        stakersCooldowns[from].amount =
          stakersCooldowns[from].amount -
          amountToRedeem.toUint184();
      }
    }

    IERC20(STAKED_TOKEN).safeTransfer(to, underlyingToRedeem);

    emit Redeem(from, to, underlyingToRedeem, amountToRedeem);
  }

  function _transfer(
    address from,
    address to,
    uint256 amount
  ) internal override {
    uint256 balanceOfFrom = balanceOf(from);
    // Sender
    _updateCurrentUnclaimedRewards(from, balanceOfFrom, true);

    // Recipient
    if (from != to) {
      uint256 balanceOfTo = balanceOf(to);
      _updateCurrentUnclaimedRewards(to, balanceOfTo, true);

      CooldownSnapshot memory previousSenderCooldown = stakersCooldowns[from];
      if (previousSenderCooldown.timestamp != 0) {
        // if cooldown was set and whole balance of sender was transferred - clear cooldown
        if (balanceOfFrom == amount) {
          delete stakersCooldowns[from];
        } else if (balanceOfFrom - amount < previousSenderCooldown.amount) {
          stakersCooldowns[from].amount = uint216(balanceOfFrom - amount);
        }
      }
    }

    super._transfer(from, to, amount);
  }
