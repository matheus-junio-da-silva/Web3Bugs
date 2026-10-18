// Project 14 — Example 32: onlyOneVaultModified
// Relevant original Solidity excerpts. Full original implementation in contracts/14.

// Original file: contracts/14/specs/harness/ControllerHarness.sol
// Original lines: 1-20;88-97
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

// BEGIN ORIGINAL LINES 88-97
  }

  function getVaultCollateralAmount(
    address owner,
    uint256 vaultId,
    uint256 i
  ) external returns (uint256) {
    MarginVault.Vault storage vault = cheapGetVault(owner, vaultId);
    return vault.collateralAmounts[i];
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

// Original file: contracts/14/contracts/core/MarginPool.sol
// Original lines: 1-55
// BEGIN ORIGINAL LINES 1-55
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

    /// @notice AddressBook module
    address public addressBook;
    /// @dev the address that has the ability to withdraw excess assets in the pool
    address public farmer;
    /// @dev mapping between an asset and the amount of the asset in the pool
    mapping(address => uint256) internal assetBalance;

    /**
     * @notice contructor
     * @param _addressBook AddressBook module
     */
    constructor(address _addressBook) public {
        require(_addressBook != address(0), "Invalid address book");

        addressBook = _addressBook;
    }

    /// @notice emits an event when marginpool receive funds from controller
    event TransferToPool(address indexed asset, address indexed user, uint256 amount);
    /// @notice emits an event when marginpool transfer funds to controller
    event TransferToUser(address indexed asset, address indexed user, uint256 amount);
    /// @notice emit event after updating the farmer address
    event FarmerUpdated(address indexed oldAddress, address indexed newAddress);
    /// @notice emit event when an asset gets harvested from the pool
    event AssetFarmed(address indexed asset, address indexed receiver, uint256 amount);

    /**
     * @notice check if the sender is the Controller module
     */
    modifier onlyController() {
        require(
            msg.sender == AddressBookInterface(addressBook).getController(),
            "MarginPool: Sender is not Controller"
        );

// END ORIGINAL EXCERPT


// Additional exact historical implementation context: contracts/14/contracts/core/Controller.sol
// Original lines: 97-110
// BEGIN ORIGINAL LINES 97-110
    mapping(address => uint256) internal accountVaultCounter;
    /// @dev mapping between an owner address and a specific vault using a vault id
    mapping(address => mapping(uint256 => MarginVault.Vault)) internal vaults;
    /// @dev mapping between an account owner and their approved or unapproved account operators
    mapping(address => mapping(address => bool)) internal operators;

    /******************************************************************** V2.0.0 storage upgrade ******************************************************/

    /// @dev mapping to map vault by each vault type
    /// borrowable pool margin vault should be set to 2, naked margin vault should be set to 1, spread/max loss vault should be set to 0
    mapping(address => mapping(uint256 => uint256)) internal vaultType;
    /// @dev mapping to store the timestamp at which the vault was last updated, will be updated in every action that changes the vault state or when calling sync()
    mapping(address => mapping(uint256 => uint256)) internal vaultLatestUpdate;

// END ORIGINAL EXCERPT

// Additional exact historical implementation context: contracts/14/contracts/core/Controller.sol
// Original lines: 611-677
// BEGIN ORIGINAL LINES 611-677
    function _runActions(Actions.ActionArgs[] memory _actions)
        internal
        returns (
            bool,
            address,
            uint256
        )
    {
        address vaultOwner;
        uint256 vaultId;
        bool vaultUpdated;

        for (uint256 i = 0; i < _actions.length; i++) {
            Actions.ActionArgs memory action = _actions[i];
            Actions.ActionType actionType = action.actionType;

            // actions except Settle, Redeem, Liquidate and Call are "Vault-updating actinos"
            // only allow update 1 vault in each operate call
            if (
                (actionType != Actions.ActionType.SettleVault) &&
                (actionType != Actions.ActionType.Redeem) &&
                (actionType != Actions.ActionType.Liquidate) &&
                (actionType != Actions.ActionType.Call)
            ) {
                // check if this action is manipulating the same vault as all other actions, if a vault has already been updated
                if (vaultUpdated) {
                    require(vaultOwner == action.owner, "C12");
                    require(vaultId == action.vaultId, "C13");
                }
                vaultUpdated = true;
                vaultId = action.vaultId;
                vaultOwner = action.owner;
            }

            if (actionType == Actions.ActionType.OpenVault) {
                _openVault(Actions._parseOpenVaultArgs(action));
            } else if (actionType == Actions.ActionType.DepositLongOption) {
                _depositLong(Actions._parseDepositArgs(action));
            } else if (actionType == Actions.ActionType.WithdrawLongOption) {
                _withdrawLong(Actions._parseWithdrawArgs(action));
            } else if (actionType == Actions.ActionType.DepositCollateral) {
                _depositCollateral(Actions._parseDepositArgs(action));
            } else if (actionType == Actions.ActionType.WithdrawCollateral) {
                _withdrawCollateral(Actions._parseWithdrawArgs(action));
            } else if (actionType == Actions.ActionType.MintShortOption) {
                _mintOtoken(Actions._parseMintArgs(action));
            } else if (actionType == Actions.ActionType.BurnShortOption) {
                _burnOtoken(Actions._parseBurnArgs(action));
            } else if (actionType == Actions.ActionType.Redeem) {
                _redeem(Actions._parseRedeemArgs(action));
            } else if (actionType == Actions.ActionType.SettleVault) {
                _settleVault(Actions._parseSettleVaultArgs(action));
            } else if (actionType == Actions.ActionType.Liquidate) {
                _liquidate(Actions._parseLiquidateArgs(action));
            } else if (actionType == Actions.ActionType.Call) {
                _call(Actions._parseCallArgs(action));
            }
        }

        return (vaultUpdated, vaultOwner, vaultId);
    }

    /**
     * @notice verify the vault final state after executing all actions
     * @param _owner account owner address
     * @param _vaultId vault id of the final vault
     */
// END ORIGINAL EXCERPT

// Additional exact historical implementation context: contracts/14/contracts/core/Controller.sol
// Original lines: 690-711
// BEGIN ORIGINAL LINES 690-711
    function _openVault(Actions.OpenVaultArgs memory _args)
        internal
        notPartiallyPaused
        onlyAuthorized(msg.sender, _args.owner)
    {
        uint256 vaultId = accountVaultCounter[_args.owner].add(1);

        require(_args.vaultId == vaultId, "C15");

        // store new vault
        accountVaultCounter[_args.owner] = vaultId;
        vaultType[_args.owner][vaultId] = borrowablePool.isWhitelistedOptionsVault(_args.owner) ? 2 : _args.vaultType;

        emit VaultOpened(_args.owner, vaultId, _args.vaultType);
    }

    /**
     * @notice deposit a long oToken into a vault
     * @dev only the account owner or operator can deposit a long oToken, cannot be called when system is partiallyPaused or fullyPaused
     * @param _args DepositArgs structure
     */
    function _depositLong(Actions.DepositArgs memory _args)
// END ORIGINAL EXCERPT
