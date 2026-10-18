// Project 14 — Example 34: optionWithdrawsRestricted
// Relevant original Solidity excerpts. Full original implementation in contracts/14.

// Original file: contracts/14/specs/harness/ControllerHarness.sol
// Original lines: 1-20;210-228;323-342;358-367
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

// BEGIN ORIGINAL LINES 210-228
  }

  function withdrawLongB(
    address owner,
    uint256 vaultId,
    address to,
    uint256 index,
    uint256 amount
  ) external {
    Actions.WithdrawArgs memory args = Actions.WithdrawArgs({
      owner: owner,
      vaultId: vaultId,
      to: to,
      asset: anOtokenB,
      index: index,
      amount: amount
    });
    _withdrawLong(args);
  }
// END ORIGINAL EXCERPT

// BEGIN ORIGINAL LINES 323-342
  }

  function burnOtokenB(
    address owner,
    uint256 vaultId,
    address from,
    uint256 index,
    uint256 amount
  ) external {
    require(smallVault(owner, vaultId, 1));
    Actions.BurnArgs memory args = Actions.BurnArgs({
      owner: owner,
      vaultId: vaultId,
      from: from,
      otoken: anOtokenB,
      index: index,
      amount: amount
    });
    _burnOtoken(args);
  }
// END ORIGINAL EXCERPT

// BEGIN ORIGINAL LINES 358-367
    - and : sed 's/delete vaults/} delete vaults/g'
  */
  function settleVault(
    address owner,
    uint256 vaultId,
    address to
  ) external {
    Actions.SettleVaultArgs memory args = Actions.SettleVaultArgs({owner: owner, vaultId: vaultId, to: to});
    _settleVault(args);
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
// Original lines: 742-769
// BEGIN ORIGINAL LINES 742-769
    function _withdrawLong(Actions.WithdrawArgs memory _args)
        internal
        notPartiallyPaused
        onlyAuthorized(msg.sender, _args.owner)
    {
        require(_checkVaultId(_args.owner, _args.vaultId), "C35");

        OtokenInterface otoken = OtokenInterface(_args.asset);

        require(now < otoken.expiryTimestamp(), "C19");

        vaults[_args.owner][_args.vaultId].removeLong(_args.asset, _args.amount, _args.index);

        MarginPoolInterface(_getPool(vaultType[_args.owner][_args.vaultId])).transferToUser(
            _args.asset,
            _args.to,
            _args.amount
        );

        emit LongOtokenWithdrawed(_args.asset, _args.owner, _args.to, _args.vaultId, _args.amount);
    }

    /**
     * @notice deposit a collateral asset into a vault
     * @dev only the account owner or operator can deposit collateral, cannot be called when system is partiallyPaused or fullyPaused
     * @param _args DepositArgs structure
     */
    function _depositCollateral(Actions.DepositArgs memory _args)
// END ORIGINAL EXCERPT

// Additional exact historical implementation context: contracts/14/contracts/core/Controller.sol
// Original lines: 863-892
// BEGIN ORIGINAL LINES 863-892
    function _burnOtoken(Actions.BurnArgs memory _args)
        internal
        notPartiallyPaused
        onlyAuthorized(msg.sender, _args.owner)
    {
        // check that vault id is valid for this vault owner
        require(_checkVaultId(_args.owner, _args.vaultId), "C35");
        // only allow vault owner or vault operator to burn otoken
        require((_args.from == msg.sender) || (_args.from == _args.owner), "C25");

        OtokenInterface otoken = OtokenInterface(_args.otoken);

        // do not allow burning expired otoken
        require(now < otoken.expiryTimestamp(), "C26");

        // remove otoken from vault
        vaults[_args.owner][_args.vaultId].removeShort(_args.otoken, _args.amount, _args.index);

        // burn otoken
        otoken.burnOtoken(_args.from, _args.amount);

        emit ShortOtokenBurned(_args.otoken, _args.owner, _args.from, _args.vaultId, _args.amount);
    }

    /**
     * @notice redeem an oToken after expiry, receiving the payout of the oToken in the collateral asset
     * @dev cannot be called when system is fullyPaused
     * @param _args RedeemArgs structure
     */
    function _redeem(Actions.RedeemArgs memory _args) internal {
// END ORIGINAL EXCERPT

// Additional exact historical implementation context: contracts/14/contracts/core/MarginPool.sol
// Original lines: 93-118
// BEGIN ORIGINAL LINES 93-118
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
