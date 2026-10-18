// Project 14 — Example 9: integrityOfAddShort
// Relevant original Solidity excerpts. Full original implementation in contracts/14.

// Original file: contracts/14/specs/harness/MarginVaultHarness.sol
// Original lines: 1-143
// BEGIN ORIGINAL LINES 1-143
pragma solidity =0.6.10;

pragma experimental ABIEncoderV2;

import {MarginVault} from '../../contracts/libs/MarginVault.sol';
import {SafeMath} from '../../contracts/packages/oz/SafeMath.sol';

contract MarginVaultHarness {
  using MarginVault for MarginVault.Vault;
  using SafeMath for uint256;

  MarginVault.Vault vault;

  function addShort(
    address _shortOtoken,
    uint256 _amount,
    uint256 _index
  ) external {
    // require(_shortOtoken != address(0)); //add this to avoid violations
    return vault.addShort(_shortOtoken, _amount, _index);
  }

  function removeShort(
    address _shortOtoken,
    uint256 _amount,
    uint256 _index
  ) external {
    return vault.removeShort(_shortOtoken, _amount, _index);
  }

  function addLong(
    address _longOtoken,
    uint256 _amount,
    uint256 _index
  ) external {
    // require(_longOtoken != address(0)); //add this to avoid violations
    return vault.addLong(_longOtoken, _amount, _index);
  }

  function removeLong(
    address _longOtoken,
    uint256 _amount,
    uint256 _index
  ) external {
    return vault.removeLong(_longOtoken, _amount, _index);
  }

  function addCollateral(
    address _collateralAsset,
    uint256 _amount,
    uint256 _index
  ) external {
    // require (_collateralAsset != address(0)); //add this to avoid violations
    return vault.addCollateral(_collateralAsset, _amount, _index);
  }

  function removeCollateral(
    address _collateralAsset,
    uint256 _amount,
    uint256 _index
  ) external {
    return vault.removeCollateral(_collateralAsset, _amount, _index);
  }

  function totalCollateral() external returns (uint256) {
    uint256 total = 0;
    for (uint256 i = 0; i < vault.collateralAmounts.length; i++) {
      total = total.add(vault.collateralAmounts[i]);
    }
    return total;
  }

  /*** collateral entity  */
  function collateralAmountLength() external returns (uint256) {
    return vault.collateralAmounts.length;
  }

  function collateralAssetsLength() external returns (uint256) {
    return vault.collateralAssets.length;
  }

  function getCollateralAmount(uint256 index) external returns (uint256) {
    return vault.collateralAmounts[index];
  }

  function getCollateralAsset(uint256 index) external returns (address) {
    return vault.collateralAssets[index];
  }

  /*** short entity  */
  function totalShortAmount() external returns (uint256) {
    uint256 total = 0;
    for (uint256 i = 0; i < vault.shortAmounts.length; i++) {
      total = total.add(vault.shortAmounts[i]);
    }
    return total;
  }

  function shortAmountLength() external returns (uint256) {
    return vault.shortAmounts.length;
  }

  function shortOtokensLength() external returns (uint256) {
    return vault.shortOtokens.length;
  }

  function getShortOtoken(uint256 index) external returns (address) {
    return vault.shortOtokens[index];
  }

  function getShortAmount(uint256 index) external returns (uint256) {
    return vault.shortAmounts[index];
  }

  /*** long entity  */

  function totalLongAmount() external returns (uint256) {
    uint256 total = 0;
    for (uint256 i = 0; i < vault.longAmounts.length; i++) {
      total = total.add(vault.longAmounts[i]);
    }
    return total;
  }

  function longAmountLength() external returns (uint256) {
    return vault.longAmounts.length;
  }

  function longOtokensLength() external returns (uint256) {
    return vault.longOtokens.length;
  }

  function getLongOtoken(uint256 index) external returns (address) {
    return vault.longOtokens[index];
  }

  function getLongAmount(uint256 index) external returns (uint256) {
    return vault.longAmounts[index];
  }

  // simulate constructor for verifying invariants at initial state
  function init_state() external {}
}
// END ORIGINAL EXCERPT

// Original file: contracts/14/contracts/libs/MarginVault.sol
// Original lines: 1-20;55-78
// BEGIN ORIGINAL LINES 1-20
/**
 * SPDX-License-Identifier: UNLICENSED
 */
pragma solidity =0.6.10;

pragma experimental ABIEncoderV2;

import {SafeMath} from "../packages/oz/SafeMath.sol";

/**
 * MarginVault Error Codes
 * V1: invalid short otoken amount
 * V2: invalid short otoken index
 * V3: short otoken address mismatch
 * V4: invalid long otoken amount
 * V5: invalid long otoken index
 * V6: long otoken address mismatch
 * V7: invalid collateral amount
 * V8: invalid collateral token index
 * V9: collateral token address mismatch
// END ORIGINAL EXCERPT

// BEGIN ORIGINAL LINES 55-78
     * @param _index index of _shortOtoken in the user's vault.shortOtokens array
     */
    function addShort(
        Vault storage _vault,
        address _shortOtoken,
        uint256 _amount,
        uint256 _index
    ) external {
        require(_amount > 0, "V1");

        // valid indexes in any array are between 0 and array.length - 1.
        // if adding an amount to an preexisting short oToken, check that _index is in the range of 0->length-1
        if ((_index == _vault.shortOtokens.length) && (_index == _vault.shortAmounts.length)) {
            _vault.shortOtokens.push(_shortOtoken);
            _vault.shortAmounts.push(_amount);
        } else {
            require((_index < _vault.shortOtokens.length) && (_index < _vault.shortAmounts.length), "V2");
            address existingShort = _vault.shortOtokens[_index];
            require((existingShort == _shortOtoken) || (existingShort == address(0)), "V3");

            _vault.shortAmounts[_index] = _vault.shortAmounts[_index].add(_amount);
            _vault.shortOtokens[_index] = _shortOtoken;
        }
    }
// END ORIGINAL EXCERPT
