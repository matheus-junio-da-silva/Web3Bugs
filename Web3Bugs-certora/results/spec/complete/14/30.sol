// Project 14 — Example 30: settleVault
// Relevant original Solidity excerpts. Full original implementation in contracts/14.

// Original file: contracts/14/specs/harness/ControllerHarness.sol
// Original lines: 1-20;97-106;133-142;358-367;371-380
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

// BEGIN ORIGINAL LINES 97-106
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

// BEGIN ORIGINAL LINES 133-142
  }

  function getVaultShortOtoken(
    address owner,
    uint256 vaultId,
    uint256 i
  ) external returns (address) {
    MarginVault.Vault storage vault = cheapGetVault(owner, vaultId);
    return vault.shortOtokens[i];
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

// BEGIN ORIGINAL LINES 371-380
    - call with extended calculator: sed 's/getExcessCollateral\(vault/getExcessCollateral\(vault.shortAmounts[0],vault.longAmounts[0],vault.collateralAmounts[0]/g'
  */
  /*function getProceed(address _owner, uint256 _vaultId) external view override returns (uint256) {
        MarginVault.Vault storage vault = cheapGetVault(_owner, _vaultId);

        (uint256 netValue, ) = calculator.getExcessCollateral(vault.shortAmounts[0],
        vault.longAmounts[0],
        vault.collateralAmounts[0]);
        return netValue;
  }*/
// END ORIGINAL EXCERPT

// Original file: contracts/14/contracts/core/Controller.sol
// Original lines: 1-20;465-475;922-979
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

// BEGIN ORIGINAL LINES 465-475
     * @return amount of collateral that can be taken out
     */
    function getProceed(address _owner, uint256 _vaultId) external view returns (uint256) {
        (MarginVault.Vault memory vault, uint256 typeVault, ) = getVaultWithDetails(_owner, _vaultId);

        (uint256 netValue, bool isExcess) = calculator.getExcessCollateral(vault, typeVault);

        if (!isExcess) return 0;

        return netValue;
    }
// END ORIGINAL EXCERPT

// BEGIN ORIGINAL LINES 922-979
     * @param _args SettleVaultArgs structure
     */
    function _settleVault(Actions.SettleVaultArgs memory _args) internal onlyAuthorized(msg.sender, _args.owner) {
        require(_checkVaultId(_args.owner, _args.vaultId), "C35");

        (MarginVault.Vault memory vault, uint256 typeVault, ) = getVaultWithDetails(_args.owner, _args.vaultId);

        OtokenInterface otoken;

        // new scope to avoid stack too deep error
        // check if there is short or long otoken in vault
        // do not allow settling vault that have no short or long otoken
        // if there is a long otoken, burn it
        // store otoken address outside of this scope
        {
            bool hasShort = _isNotEmpty(vault.shortOtokens);
            bool hasLong = _isNotEmpty(vault.longOtokens);

            require(hasShort || hasLong, "C30");

            otoken = hasShort ? OtokenInterface(vault.shortOtokens[0]) : OtokenInterface(vault.longOtokens[0]);

            if (hasLong) {
                OtokenInterface longOtoken = OtokenInterface(vault.longOtokens[0]);

                longOtoken.burnOtoken(_getPool(vaultType[_args.owner][_args.vaultId]), vault.longAmounts[0]);
            }
        }

        (address collateral, address underlying, address strike, uint256 expiry) = _getOtokenDetails(address(otoken));

        // do not allow settling vault with un-expired otoken
        require(now >= expiry, "C31");
        require(_canSettleAssets(underlying, strike, collateral, expiry), "C29");

        (uint256 payout, bool isValidVault) = calculator.getExcessCollateral(vault, typeVault);

        // require that vault is valid (has excess collateral) before settling
        // to avoid allowing settling undercollateralized naked margin vault
        require(isValidVault, "C32");

        delete vaults[_args.owner][_args.vaultId];

        if (typeVault == 1) {
            nakedPoolBalance[collateral] = nakedPoolBalance[collateral].sub(payout);
        }

        MarginPoolInterface(_getPool(vaultType[_args.owner][_args.vaultId])).transferToUser(
            collateral,
            _args.to,
            payout
        );

        uint256 vaultId = _args.vaultId;
        address payoutRecipient = _args.to;

        emit VaultSettled(_args.owner, address(otoken), payoutRecipient, payout, vaultId, typeVault);
    }
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
// Original lines: 467-480
// BEGIN ORIGINAL LINES 467-480
    function getProceed(address _owner, uint256 _vaultId) external view returns (uint256) {
        (MarginVault.Vault memory vault, uint256 typeVault, ) = getVaultWithDetails(_owner, _vaultId);

        (uint256 netValue, bool isExcess) = calculator.getExcessCollateral(vault, typeVault);

        if (!isExcess) return 0;

        return netValue;
    }

    /**
     * @notice check if a vault is liquidatable in a specific round id
     * @param _owner vault owner address
     * @param _vaultId vault id to check
// END ORIGINAL EXCERPT

// Additional exact historical implementation context: contracts/14/contracts/core/Controller.sol
// Original lines: 924-975
// BEGIN ORIGINAL LINES 924-975
    function _settleVault(Actions.SettleVaultArgs memory _args) internal onlyAuthorized(msg.sender, _args.owner) {
        require(_checkVaultId(_args.owner, _args.vaultId), "C35");

        (MarginVault.Vault memory vault, uint256 typeVault, ) = getVaultWithDetails(_args.owner, _args.vaultId);

        OtokenInterface otoken;

        // new scope to avoid stack too deep error
        // check if there is short or long otoken in vault
        // do not allow settling vault that have no short or long otoken
        // if there is a long otoken, burn it
        // store otoken address outside of this scope
        {
            bool hasShort = _isNotEmpty(vault.shortOtokens);
            bool hasLong = _isNotEmpty(vault.longOtokens);

            require(hasShort || hasLong, "C30");

            otoken = hasShort ? OtokenInterface(vault.shortOtokens[0]) : OtokenInterface(vault.longOtokens[0]);

            if (hasLong) {
                OtokenInterface longOtoken = OtokenInterface(vault.longOtokens[0]);

                longOtoken.burnOtoken(_getPool(vaultType[_args.owner][_args.vaultId]), vault.longAmounts[0]);
            }
        }

        (address collateral, address underlying, address strike, uint256 expiry) = _getOtokenDetails(address(otoken));

        // do not allow settling vault with un-expired otoken
        require(now >= expiry, "C31");
        require(_canSettleAssets(underlying, strike, collateral, expiry), "C29");

        (uint256 payout, bool isValidVault) = calculator.getExcessCollateral(vault, typeVault);

        // require that vault is valid (has excess collateral) before settling
        // to avoid allowing settling undercollateralized naked margin vault
        require(isValidVault, "C32");

        delete vaults[_args.owner][_args.vaultId];

        if (typeVault == 1) {
            nakedPoolBalance[collateral] = nakedPoolBalance[collateral].sub(payout);
        }

        MarginPoolInterface(_getPool(vaultType[_args.owner][_args.vaultId])).transferToUser(
            collateral,
            _args.to,
            payout
        );

        uint256 vaultId = _args.vaultId;
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
