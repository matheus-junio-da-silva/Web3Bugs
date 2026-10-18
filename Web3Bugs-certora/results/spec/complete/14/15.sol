// Project 14 — Example 15: putOptionsPreExpiryCase1StartingWithAllCases
// Relevant original Solidity excerpts. Full original implementation in contracts/14.

// Original file: contracts/14/specs/harness/ControllerHarnessExtra.sol
// Original lines: 1-36
// BEGIN ORIGINAL LINES 1-36
pragma solidity =0.6.10;

pragma experimental ABIEncoderV2;

import 'specs/harness/ControllerHarness.sol';

interface ExtendedERC20 {
  function havocTotalSupply(uint256) external;

  function havocVault(
    address owner,
    uint256 vaultId,
    uint256 i,
    uint256 newShortAmount,
    uint256 newLongAmount,
    uint256 newcollateralAmount
  ) external;
}

/**
    An additional harness over the controller to allow checking the no-bankruptcy rules.
 */
contract ControllerHarnessExtra is ControllerHarness {
  function havocVault(
    address owner,
    uint256 vaultId,
    uint256 i,
    uint256 newShortAmount,
    uint256 newLongAmount,
    uint256 newcollateralAmount
  ) external {
    MarginVault.Vault storage vault = cheapGetVault(owner, vaultId);
    vault.shortAmounts[i] = newShortAmount;
    vault.longAmounts[i] = newLongAmount;
    vault.collateralAmounts[i] = newcollateralAmount;
  }
// END ORIGINAL EXCERPT

// Original file: contracts/14/specs/harness/ControllerHarness.sol
// Original lines: 1-20;44-51;88-115
// BEGIN ORIGINAL LINES 1-20
pragma solidity =0.6.10;

pragma experimental ABIEncoderV2;

import '../../contracts/core/Controller.sol';
import {ERC20Interface} from '../../contracts/interfaces/ERC20Interface.sol';
import {MarginVault} from '../../contracts/libs/MarginVault.sol';
import {OtokenInterface} from '../../contracts/interfaces/OtokenInterface.sol';

contract ControllerHarness is Controller {
  /** 
    We work on each function independently.
    We also need to make it virtual:
    sed 's/function _runActions\(Actions.ActionArgs[] memory _actions\)/function _runActions\(Actions.ActionArgs[] memory _actions\) virtual/g'
   */
  function _runActions(Actions.ActionArgs[] memory _actions)
    internal
    override
    returns (
      bool,
// END ORIGINAL EXCERPT

// BEGIN ORIGINAL LINES 44-51
  }

  function assetTotalSupply(address asset) external view returns (uint256) {
    if (asset == anOtokenA) return ERC20Interface(anOtokenA).totalSupply();
    else if (asset == anOtokenB) return ERC20Interface(anOtokenB).totalSupply();
    else if (asset == dummyERC20C) return ERC20Interface(dummyERC20C).totalSupply();
    else return ERC20Interface(asset).totalSupply();
  }
// END ORIGINAL EXCERPT

// BEGIN ORIGINAL LINES 88-115
  }

  function getVaultCollateralAmount(
    address owner,
    uint256 vaultId,
    uint256 i
  ) external returns (uint256) {
    MarginVault.Vault storage vault = cheapGetVault(owner, vaultId);
    return vault.collateralAmounts[i];
  }

  function getVaultCollateralAsset(
    address owner,
    uint256 vaultId,
    uint256 i
  ) external returns (address) {
    MarginVault.Vault storage vault = cheapGetVault(owner, vaultId);
    return vault.collateralAssets[i];
  }

  function getVaultLongAmount(
    address owner,
    uint256 vaultId,
    uint256 i
  ) external returns (uint256) {
    MarginVault.Vault storage vault = cheapGetVault(owner, vaultId);
    return vault.longAmounts[i];
  }
// END ORIGINAL EXCERPT

// Original file: contracts/14/contracts/core/Controller.sol
// Original lines: 1-55
// BEGIN ORIGINAL LINES 1-55
/**
 * SPDX-License-Identifier: UNLICENSED
 */
pragma solidity =0.6.10;

pragma experimental ABIEncoderV2;

import {OwnableUpgradeSafe} from "../packages/oz/upgradeability/OwnableUpgradeSafe.sol";
import {ReentrancyGuardUpgradeSafe} from "../packages/oz/upgradeability/ReentrancyGuardUpgradeSafe.sol";
import {Initializable} from "../packages/oz/upgradeability/Initializable.sol";
import {SafeMath} from "../packages/oz/SafeMath.sol";
import {MarginVault} from "../libs/MarginVault.sol";
import {Actions} from "../libs/Actions.sol";
import {AddressBookInterface} from "../interfaces/AddressBookInterface.sol";
import {ERC20Interface} from "../interfaces/ERC20Interface.sol";
import {OtokenInterface} from "../interfaces/OtokenInterface.sol";
import {MarginCalculatorInterface} from "../interfaces/MarginCalculatorInterface.sol";
import {OracleInterface} from "../interfaces/OracleInterface.sol";
import {WhitelistInterface} from "../interfaces/WhitelistInterface.sol";
import {MarginPoolInterface} from "../interfaces/MarginPoolInterface.sol";
import {CalleeInterface} from "../interfaces/CalleeInterface.sol";

/**
 * Controller Error Codes
 * C1: sender is not full pauser
 * C2: sender is not partial pauser
 * C3: callee is not a whitelisted address
 * C4: system is partially paused
 * C5: system is fully paused
 * C6: msg.sender is not authorized to run action
 * C7: invalid addressbook address
 * C8: invalid owner address
 * C12: can not run actions for different owners
 * C13: can not run actions on different vaults
 * C14: invalid final vault state
 * C15: can not run actions on inexistent vault
 * C16: cannot deposit long otoken from this address
 * C17: otoken is not whitelisted to be used as collateral
 * C18: otoken used as collateral is already expired
 * C19: can not withdraw an expired otoken
 * C20: cannot deposit collateral from this address
 * C21: asset is not whitelisted to be used as collateral
 * C22: can not withdraw collateral from a vault with an expired short otoken
 * C23: otoken is not whitelisted to be minted
 * C24: can not mint expired otoken
 * C25: cannot burn from this address
 * C26: can not burn expired otoken
 * C27: otoken is not whitelisted to be redeemed
 * C28: can not redeem un-expired otoken
 * C29: asset prices not finalized yet
 * C30: can't settle vault with no otoken
 * C31: can not settle vault with un-expired otoken
 * C32: can not settle undercollateralized vault
 * C33: can not liquidate vault
 * C34: can not leave less than collateral dust
// END ORIGINAL EXCERPT


// Additional exact historical implementation context: contracts/14/specs/harness/MarginPoolHarness.sol
// Original lines: 1-15
// BEGIN ORIGINAL LINES 1-15
pragma solidity =0.6.10;

pragma experimental ABIEncoderV2;

import '../../contracts/core/MarginPool.sol';

contract MarginPoolHarness is MarginPool {
  constructor(address _addressBook) public MarginPool(_addressBook) {}

  mapping(address => uint256) internal assetBalanceHavoc;

  function havocSystemBalance(address _asset) public {
    assetBalance[_asset] = assetBalanceHavoc[_asset];
  }
}
// END ORIGINAL EXCERPT

// Additional exact historical implementation context: contracts/14/specs/harness/OtokenHarnessA.sol
// Original lines: 1-8
// BEGIN ORIGINAL LINES 1-8
pragma solidity ^0.6.0;
import '../../contracts/core/Otoken.sol';

contract OtokenHarnessA is Otoken {
  function havocTotalSupply(uint256 newVal) public {
    _totalSupply = newVal;
  }
}
// END ORIGINAL EXCERPT
