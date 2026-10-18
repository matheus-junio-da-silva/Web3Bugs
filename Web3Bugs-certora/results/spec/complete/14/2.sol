// Project 14 — Example 2: validVault
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
// Original lines: 1-55
// BEGIN ORIGINAL LINES 1-55
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
 */

/**
 * @title MarginVault
 * @author Opyn Team
 * @notice A library that provides the Controller with a Vault struct and the functions that manipulate vaults.
 * Vaults describe discrete position combinations of long options, short options, and collateral assets that a user can have.
 */
library MarginVault {
    using SafeMath for uint256;

    // vault is a struct of 6 arrays that describe a position a user has, a user can have multiple vaults.
    struct Vault {
        // addresses of oTokens a user has shorted (i.e. written) against this vault
        address[] shortOtokens;
        // addresses of oTokens a user has bought and deposited in this vault
        // user can be long oTokens without opening a vault (e.g. by buying on a DEX)
        // generally, long oTokens will be 'deposited' in vaults to act as collateral in order to write oTokens against (i.e. in spreads)
        address[] longOtokens;
        // addresses of other ERC-20s a user has deposited as collateral in this vault
        address[] collateralAssets;
        // quantity of oTokens minted/written for each oToken address in shortOtokens
        uint256[] shortAmounts;
        // quantity of oTokens owned and held in the vault for each oToken address in longOtokens
        uint256[] longAmounts;
        // quantity of ERC-20 deposited as collateral in the vault for each ERC-20 address in collateralAssets
        uint256[] collateralAmounts;
    }

    /**
     * @dev increase the short oToken balance in a vault when a new oToken is minted
     * @param _vault vault to add or increase the short position in
     * @param _shortOtoken address of the _shortOtoken being minted from the user's vault
     * @param _amount number of _shortOtoken being minted from the user's vault
     * @param _index index of _shortOtoken in the user's vault.shortOtokens array
// END ORIGINAL EXCERPT
