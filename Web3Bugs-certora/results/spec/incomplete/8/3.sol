// Original Solidity excerpt: contracts/8/src/ATokenVault.sol:359-403
    function maxDeposit(address) public view override(ERC4626Upgradeable, IATokenVault) returns (uint256) {
        return _maxAssetsSuppliableToAave();
    }

    /// @inheritdoc IATokenVault
    function maxMint(address) public view override(ERC4626Upgradeable, IATokenVault) returns (uint256) {
        return _convertToShares(_maxAssetsSuppliableToAave(), MathUpgradeable.Rounding.Down);
    }

    /// @inheritdoc IATokenVault
    function maxWithdraw(address owner) public view override(ERC4626Upgradeable, IATokenVault) returns (uint256) {
        uint256 maxWithdrawable = _maxAssetsWithdrawableFromAave();
        return
            maxWithdrawable == 0 ? 0 : maxWithdrawable.min(_convertToAssets(balanceOf(owner), MathUpgradeable.Rounding.Down));
    }

    /// @inheritdoc IATokenVault
    function maxRedeem(address owner) public view override(ERC4626Upgradeable, IATokenVault) returns (uint256) {
        uint256 maxWithdrawable = _maxAssetsWithdrawableFromAave();
        return
            maxWithdrawable == 0 ? 0 : _convertToShares(maxWithdrawable, MathUpgradeable.Rounding.Down).min(balanceOf(owner));
    }

    /// @inheritdoc IATokenVault
    function previewDeposit(uint256 assets) public view override(ERC4626Upgradeable, IATokenVault) returns (uint256) {
        return _convertToShares(_maxAssetsSuppliableToAave().min(assets), MathUpgradeable.Rounding.Down);
    }

    /// @inheritdoc IATokenVault
    function previewMint(uint256 shares) public view override(ERC4626Upgradeable, IATokenVault) returns (uint256) {
        return _convertToAssets(shares, MathUpgradeable.Rounding.Up).min(_maxAssetsSuppliableToAave());
    }

    /// @inheritdoc IATokenVault
    function previewWithdraw(uint256 assets) public view override(ERC4626Upgradeable, IATokenVault) returns (uint256) {
        uint256 maxWithdrawable = _maxAssetsWithdrawableFromAave();
        return maxWithdrawable == 0 ? 0 : _convertToShares(maxWithdrawable.min(assets), MathUpgradeable.Rounding.Up);
    }

    /// @inheritdoc IATokenVault
    function previewRedeem(uint256 shares) public view override(ERC4626Upgradeable, IATokenVault) returns (uint256) {
        uint256 maxWithdrawable = _maxAssetsWithdrawableFromAave();
        return maxWithdrawable == 0 ? 0 : _convertToAssets(shares, MathUpgradeable.Rounding.Down).min(maxWithdrawable);
    }


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

// Original Solidity excerpt: contracts/8/src/ATokenVault.sol:571-616
    function _maxAssetsSuppliableToAave() internal view returns (uint256) {
        // returns 0 if reserve is not active, frozen, or paused
        // returns max uint256 value if supply cap is 0 (not capped)
        // returns supply cap - current amount supplied as max suppliable if there is a supply cap for this reserve

        AaveDataTypes.ReserveData memory reserveData = AAVE_POOL.getReserveData(address(UNDERLYING));

        uint256 reserveConfigMap = reserveData.configuration.data;
        uint256 supplyCap = (reserveConfigMap & ~AAVE_SUPPLY_CAP_MASK) >> AAVE_SUPPLY_CAP_BIT_POSITION;

        if (
            (reserveConfigMap & ~AAVE_ACTIVE_MASK == 0) ||
            (reserveConfigMap & ~AAVE_FROZEN_MASK != 0) ||
            (reserveConfigMap & ~AAVE_PAUSED_MASK != 0)
        ) {
            return 0;
        } else if (supplyCap == 0) {
            return type(uint256).max;
        } else {
            // Reserve's supply cap - current amount supplied
            // See similar logic in Aave v3 ValidationLogic library, in the validateSupply function
            // https://github.com/aave/aave-v3-core/blob/a00f28e3ad7c0e4a369d8e06e0ac9fd0acabcab7/contracts/protocol/libraries/logic/ValidationLogic.sol#L71-L78
            uint256 currentSupply = WadRayMath.rayMul(
                (ATOKEN.scaledTotalSupply() + uint256(reserveData.accruedToTreasury)),
                reserveData.liquidityIndex
            );
            uint256 supplyCapWithDecimals = supplyCap * 10 ** decimals();
            return supplyCapWithDecimals > currentSupply ? supplyCapWithDecimals - currentSupply : 0;
        }
    }

    function _maxAssetsWithdrawableFromAave() internal view returns (uint256) {
        // returns 0 if reserve is not active, or paused
        // otherwise, returns available liquidity

        AaveDataTypes.ReserveData memory reserveData = AAVE_POOL.getReserveData(address(UNDERLYING));

        uint256 reserveConfigMap = reserveData.configuration.data;

        if ((reserveConfigMap & ~AAVE_ACTIVE_MASK == 0) || (reserveConfigMap & ~AAVE_PAUSED_MASK != 0)) {
            return 0;
        } else {
            return UNDERLYING.balanceOf(address(ATOKEN));
        }
    }


// Original Solidity excerpt: contracts/8/src/ATokenVaultStorage.sol:14-20
    struct Storage {
        // total aToken incl. fees
        uint128 lastVaultBalance;
        // fees accrued since last updated
        uint128 accumulatedFees;
        // Deprecated storage gap
        uint40 __deprecated_gap;

