// Project 14 — Example 26: validBalanceOfTheSystem
// Relevant original Solidity excerpts. Full original implementation in contracts/14.

// Original file: contracts/14/specs/harness/ControllerHarness.sol
// Original lines: 1-55
// BEGIN ORIGINAL LINES 1-55
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
      address,
      uint256
    )
  {}

  /* will be added by harness script */
  /*
  address public anOtokenA;
  address public anOtokenB;
  address public dummyERC20C;
  */
  function assetBalanceOf(address asset, address a) external view returns (uint256) {
    if (asset == anOtokenA) return ERC20Interface(anOtokenA).balanceOf(a);
    else if (asset == anOtokenB) return ERC20Interface(anOtokenB).balanceOf(a);
    else if (asset == dummyERC20C) return ERC20Interface(dummyERC20C).balanceOf(a);
    else return ERC20Interface(asset).balanceOf(a);
  }

  function assetBalanceOfPool(address asset) external view returns (uint256) {
    if (asset == anOtokenA) return ERC20Interface(anOtokenA).balanceOf(address(pool));
    else if (asset == anOtokenB) return ERC20Interface(anOtokenB).balanceOf(address(pool));
    else if (asset == dummyERC20C) return ERC20Interface(dummyERC20C).balanceOf(address(pool));
    else return ERC20Interface(asset).balanceOf(address(pool));
  }

  function assetTotalSupply(address asset) external view returns (uint256) {
    if (asset == anOtokenA) return ERC20Interface(anOtokenA).totalSupply();
    else if (asset == anOtokenB) return ERC20Interface(anOtokenB).totalSupply();
    else if (asset == dummyERC20C) return ERC20Interface(dummyERC20C).totalSupply();
    else return ERC20Interface(asset).totalSupply();
  }

  function smallVault(
    address owner,
    uint256 vaultId,
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

// Original file: contracts/14/contracts/core/MarginPool.sol
// Original lines: 1-20;109-113
// BEGIN ORIGINAL LINES 1-20
/**
 * SPDX-License-Identifier: UNLICENSED
 */
pragma solidity =0.6.10;

import {ERC20Interface} from "../interfaces/ERC20Interface.sol";
import {AddressBookInterface} from "../interfaces/AddressBookInterface.sol";
import {SafeMath} from "../packages/oz/SafeMath.sol";
import {SafeERC20} from "../packages/oz/SafeERC20.sol";
import {Ownable} from "../packages/oz/Ownable.sol";

/**
 * @author Opyn Team
 * @title MarginPool
 * @notice Contract that holds all protocol funds
 */
contract MarginPool is Ownable {
    using SafeMath for uint256;
    using SafeERC20 for ERC20Interface;

// END ORIGINAL EXCERPT

// BEGIN ORIGINAL LINES 109-113
     * @return asset balance
     */
    function getStoredBalance(address _asset) external view returns (uint256) {
        return assetBalance[_asset];
    }
// END ORIGINAL EXCERPT


// Additional exact historical implementation context: contracts/14/contracts/core/MarginPool.sol
// Original lines: 20-28
// BEGIN ORIGINAL LINES 20-28

    /// @notice AddressBook module
    address public addressBook;
    /// @dev the address that has the ability to withdraw excess assets in the pool
    address public farmer;
    /// @dev mapping between an asset and the amount of the asset in the pool
    mapping(address => uint256) internal assetBalance;

    /**
// END ORIGINAL EXCERPT

// Additional exact historical implementation context: contracts/14/contracts/core/MarginPool.sol
// Original lines: 74-118
// BEGIN ORIGINAL LINES 74-118
    function transferToPool(
        address _asset,
        address _user,
        uint256 _amount
    ) public onlyController {
        require(_amount > 0, "MarginPool: transferToPool amount is equal to 0");
        assetBalance[_asset] = assetBalance[_asset].add(_amount);

        // transfer _asset _amount from _user to pool
        ERC20Interface(_asset).safeTransferFrom(_user, address(this), _amount);
        emit TransferToPool(_asset, _user, _amount);
    }

    /**
     * @notice transfers an asset from the pool to a user
     * @param _asset address of the asset to transfer
     * @param _user address of the user to transfer assets to
     * @param _amount amount of the token to transfer to _user
     */
    function transferToUser(
        address _asset,
        address _user,
        uint256 _amount
    ) public onlyController {
        require(_user != address(this), "MarginPool: cannot transfer assets to oneself");
        assetBalance[_asset] = assetBalance[_asset].sub(_amount);

        // transfer _asset _amount from pool to _user
        ERC20Interface(_asset).safeTransfer(_user, _amount);
        emit TransferToUser(_asset, _user, _amount);
    }

    /**
     * @notice get the stored balance of an asset
     * @param _asset asset address
     * @return asset balance
     */
    function getStoredBalance(address _asset) external view returns (uint256) {
        return assetBalance[_asset];
    }

    /**
     * @notice transfers multiple assets from users to the pool
     * @param _asset addresses of the assets to transfer
     * @param _user addresses of the users to transfer assets to
// END ORIGINAL EXCERPT
