// Project 14 — Example 18: callOptionsPreExpiry
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
// Original lines: 1-20;1043-1049
// BEGIN ORIGINAL LINES 1-20
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
// END ORIGINAL EXCERPT

// BEGIN ORIGINAL LINES 1043-1049
     * @param _args Call action
     */
    function _call(Actions.CallArgs memory _args) internal notPartiallyPaused onlyWhitelistedCallee(_args.callee) {
        CalleeInterface(_args.callee).callFunction(msg.sender, _args.data);

        emit CallExecuted(msg.sender, _args.callee, _args.data);
    }
// END ORIGINAL EXCERPT
