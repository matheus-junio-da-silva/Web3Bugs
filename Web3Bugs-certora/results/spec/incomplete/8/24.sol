// Original Solidity excerpt: contracts/8/src/ATokenVault.sol:6-29
import {ERC4626Upgradeable} from "@openzeppelin-upgradeable/token/ERC20/extensions/ERC4626Upgradeable.sol";
import {OwnableUpgradeable} from "@openzeppelin-upgradeable/access/OwnableUpgradeable.sol";
import {SafeERC20Upgradeable} from "@openzeppelin-upgradeable/token/ERC20/utils/SafeERC20Upgradeable.sol";
import {IERC20Upgradeable} from "@openzeppelin-upgradeable/interfaces/IERC20Upgradeable.sol";
import {EIP712Upgradeable} from "@openzeppelin-upgradeable/utils/cryptography/EIP712Upgradeable.sol";
import {MathUpgradeable} from "@openzeppelin-upgradeable/utils/math/MathUpgradeable.sol";
import {IncentivizedERC20} from "@aave-v3-core/protocol/tokenization/base/IncentivizedERC20.sol";
import {IPoolAddressesProvider} from "@aave-v3-core/interfaces/IPoolAddressesProvider.sol";
import {IPool} from "@aave-v3-core/interfaces/IPool.sol";
import {IAToken} from "@aave-v3-core/interfaces/IAToken.sol";
import {DataTypes as AaveDataTypes} from "@aave-v3-core/protocol/libraries/types/DataTypes.sol";
import {WadRayMath} from "@aave-v3-core/protocol/libraries/math/WadRayMath.sol";
import {IRewardsController} from "@aave-v3-periphery/rewards/interfaces/IRewardsController.sol";
import {IATokenVault} from "./interfaces/IATokenVault.sol";
import {MetaTxHelpers} from "./libraries/MetaTxHelpers.sol";
import "./libraries/Constants.sol";
import {ATokenVaultStorage} from "./ATokenVaultStorage.sol";

/**
 * @title ATokenVault
 * @author Aave Protocol
 * @notice An ERC-4626 vault for Aave V3, with support to add a fee on yield earned.
 */
contract ATokenVault is ERC4626Upgradeable, OwnableUpgradeable, EIP712Upgradeable, ATokenVaultStorage, IATokenVault {

// Original Solidity excerpt: contracts/8/src/ATokenVault.sol:460-477
    function totalAssets() public view override(ERC4626Upgradeable, IATokenVault) returns (uint256) {
        // Report only the total assets net of fees, for vault share logic
        return ATOKEN.balanceOf(address(this)) - getClaimableFees();
    }

    /// @inheritdoc IATokenVault
    function getClaimableFees() public view override returns (uint256) {
        uint256 newVaultBalance = ATOKEN.balanceOf(address(this));

        // Skip computation if there is no yield
        if (newVaultBalance <= _s.lastVaultBalance) {
            return _s.accumulatedFees;
        }

        uint256 newYield = newVaultBalance - _s.lastVaultBalance;
        uint256 newFees = newYield.mulDiv(_s.fee, SCALE, MathUpgradeable.Rounding.Down);

        return _s.accumulatedFees + newFees;

// Original Solidity excerpt: contracts/8/src/ATokenVaultStorage.sol:12-22
    mapping(address => uint256) internal _sigNonces;

    struct Storage {
        // total aToken incl. fees
        uint128 lastVaultBalance;
        // fees accrued since last updated
        uint128 accumulatedFees;
        // Deprecated storage gap
        uint40 __deprecated_gap;
        // as a fraction of 1e18
        uint64 fee;

