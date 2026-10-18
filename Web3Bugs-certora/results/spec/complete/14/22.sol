// Project 14 — Example 22: validBalanceTotalCollateral
// Relevant original Solidity excerpts. Full original implementation in contracts/14.

// Original file: contracts/14/specs/harness/ControllerHarness.sol
// Original lines: 1-20;51-66;88-106;142-151
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

// BEGIN ORIGINAL LINES 51-66
  }

  function smallVault(
    address owner,
    uint256 vaultId,
    uint256 c
  ) public view returns (bool) {
    MarginVault.Vault storage _vault = cheapGetVault(owner, vaultId);
    return
      _vault.shortOtokens.length <= c &&
      _vault.longOtokens.length <= c &&
      _vault.collateralAssets.length <= c &&
      _vault.longAmounts.length <= c &&
      _vault.shortAmounts.length <= c &&
      _vault.collateralAmounts.length <= c;
  }
// END ORIGINAL EXCERPT

// BEGIN ORIGINAL LINES 88-106
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
// END ORIGINAL EXCERPT

// BEGIN ORIGINAL LINES 142-151
  }

  function isVaultExpired(address owner, uint256 vaultId) external view returns (bool) {
    MarginVault.Vault storage vault = cheapGetVault(owner, vaultId);
    bool hasShorts = _isNotEmpty(vault.shortOtokens);
    bool hasLongs = _isNotEmpty(vault.longOtokens);
    address otoken = hasShorts ? vault.shortOtokens[0] : vault.longOtokens[0];
    (, , , , uint256 expiry, ) = OtokenInterface(otoken).getOtokenDetails();
    return ((hasShorts || hasLongs) && now >= expiry);
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
// Original lines: 769-839
// BEGIN ORIGINAL LINES 769-839
    function _depositCollateral(Actions.DepositArgs memory _args)
        internal
        notPartiallyPaused
        onlyAuthorized(msg.sender, _args.owner)
    {
        require(_checkVaultId(_args.owner, _args.vaultId), "C35");
        // only allow vault owner or vault operator to deposit collateral
        require((_args.from == msg.sender) || (_args.from == _args.owner), "C20");

        require(whitelist.isWhitelistedCollateral(_args.asset), "C21");

        (, uint256 typeVault, ) = getVaultWithDetails(_args.owner, _args.vaultId);

        if (typeVault == 1) {
            nakedPoolBalance[_args.asset] = nakedPoolBalance[_args.asset].add(_args.amount);

            require(nakedPoolBalance[_args.asset] <= nakedCap[_args.asset], "C37");
        }

        vaults[_args.owner][_args.vaultId].addCollateral(_args.asset, _args.amount, _args.index);

        MarginPoolInterface(_getPool(vaultType[_args.owner][_args.vaultId])).transferToPool(
            _args.asset,
            _args.from,
            _args.amount
        );

        emit CollateralAssetDeposited(_args.asset, _args.owner, _args.from, _args.vaultId, _args.amount);
    }

    /**
     * @notice withdraw a collateral asset from a vault
     * @dev only the account owner or operator can withdraw collateral, cannot be called when system is partiallyPaused or fullyPaused
     * @param _args WithdrawArgs structure
     */
    function _withdrawCollateral(Actions.WithdrawArgs memory _args)
        internal
        notPartiallyPaused
        onlyAuthorized(msg.sender, _args.owner)
    {
        require(_checkVaultId(_args.owner, _args.vaultId), "C35");

        (MarginVault.Vault memory vault, uint256 typeVault, ) = getVaultWithDetails(_args.owner, _args.vaultId);

        if (_isNotEmpty(vault.shortOtokens)) {
            OtokenInterface otoken = OtokenInterface(vault.shortOtokens[0]);

            require(now < otoken.expiryTimestamp(), "C22");
        }

        if (typeVault == 1) {
            nakedPoolBalance[_args.asset] = nakedPoolBalance[_args.asset].sub(_args.amount);
        }

        vaults[_args.owner][_args.vaultId].removeCollateral(_args.asset, _args.amount, _args.index);

        MarginPoolInterface(_getPool(vaultType[_args.owner][_args.vaultId])).transferToUser(
            _args.asset,
            _args.to,
            _args.amount
        );

        emit CollateralAssetWithdrawed(_args.asset, _args.owner, _args.to, _args.vaultId, _args.amount);
    }

    /**
     * @notice mint short oTokens from a vault which creates an obligation that is recorded in the vault
     * @dev only the account owner or operator can mint an oToken, cannot be called when system is partiallyPaused or fullyPaused
     * @param _args MintArgs structure
     */
    function _mintOtoken(Actions.MintArgs memory _args)
// END ORIGINAL EXCERPT

// Additional exact historical implementation context: contracts/14/contracts/core/MarginPool.sol
// Original lines: 26-30
// BEGIN ORIGINAL LINES 26-30
    mapping(address => uint256) internal assetBalance;

    /**
     * @notice contructor
     * @param _addressBook AddressBook module
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
