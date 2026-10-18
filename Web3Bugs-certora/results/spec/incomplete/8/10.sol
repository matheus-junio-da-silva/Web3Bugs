// Original Solidity excerpt: contracts/8/src/ATokenVault.sol:102-108
    function deposit(uint256 assets, address receiver) public override(ERC4626Upgradeable, IATokenVault) returns (uint256) {
        return _handleDeposit(assets, receiver, msg.sender, false);
    }

    /// @inheritdoc IATokenVault
    function depositATokens(uint256 assets, address receiver) public override returns (uint256) {
        return _handleDeposit(assets, receiver, msg.sender, true);

// Original Solidity excerpt: contracts/8/src/ATokenVault.sol:170-176
    function mint(uint256 shares, address receiver) public override(ERC4626Upgradeable, IATokenVault) returns (uint256) {
        return _handleMint(shares, receiver, msg.sender, false);
    }

    /// @inheritdoc IATokenVault
    function mintWithATokens(uint256 shares, address receiver) public override returns (uint256) {
        return _handleMint(shares, receiver, msg.sender, true);

// Original Solidity excerpt: contracts/8/src/ATokenVault.sol:231-241
    function withdraw(
        uint256 assets,
        address receiver,
        address owner
    ) public override(ERC4626Upgradeable, IATokenVault) returns (uint256) {
        return _handleWithdraw(assets, receiver, owner, msg.sender, false);
    }

    /// @inheritdoc IATokenVault
    function withdrawATokens(uint256 assets, address receiver, address owner) public override returns (uint256) {
        return _handleWithdraw(assets, receiver, owner, msg.sender, true);

// Original Solidity excerpt: contracts/8/src/ATokenVault.sol:296-306
    function redeem(
        uint256 shares,
        address receiver,
        address owner
    ) public override(ERC4626Upgradeable, IATokenVault) returns (uint256) {
        return _handleRedeem(shares, receiver, owner, msg.sender, false);
    }

    /// @inheritdoc IATokenVault
    function redeemAsATokens(uint256 shares, address receiver, address owner) public override returns (uint256) {
        return _handleRedeem(shares, receiver, owner, msg.sender, true);

// Original Solidity excerpt: contracts/8/src/ATokenVault.sol:383-403
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


// Original Solidity excerpt: contracts/8/src/ATokenVault.sol:525-566
    function _handleDeposit(uint256 assets, address receiver, address depositor, bool asAToken) internal returns (uint256) {
        if (!asAToken) require(assets <= maxDeposit(receiver), "DEPOSIT_EXCEEDS_MAX");
        _accrueYield();
        uint256 shares = super.previewDeposit(assets);
        require(shares != 0, "ZERO_SHARES"); // Check for rounding error since we round down in previewDeposit.
        _baseDeposit(_convertToAssets(shares, MathUpgradeable.Rounding.Up), shares, depositor, receiver, asAToken);
        return shares;
    }

    function _handleMint(uint256 shares, address receiver, address depositor, bool asAToken) internal returns (uint256) {
        if (!asAToken) require(shares <= maxMint(receiver), "MINT_EXCEEDS_MAX");
        _accrueYield();
        uint256 assets = super.previewMint(shares); // No need to check for rounding error, previewMint rounds up.
        _baseDeposit(assets, shares, depositor, receiver, asAToken);
        return assets;
    }

    function _handleWithdraw(
        uint256 assets,
        address receiver,
        address owner,
        address allowanceTarget,
        bool asAToken
    ) internal returns (uint256) {
        _accrueYield();
        require(assets <= maxWithdraw(owner), "WITHDRAW_EXCEEDS_MAX");
        uint256 shares = super.previewWithdraw(assets); // No need to check for rounding error, previewWithdraw rounds up.
        _baseWithdraw(assets, shares, owner, receiver, allowanceTarget, asAToken);
        return shares;
    }

    function _handleRedeem(
        uint256 shares,
        address receiver,
        address owner,
        address allowanceTarget,
        bool asAToken
    ) internal returns (uint256) {
        _accrueYield();
        require(shares <= maxRedeem(owner), "REDEEM_EXCEEDS_MAX");
        uint256 assets = super.previewRedeem(shares);
        require(assets != 0, "ZERO_ASSETS"); // Check for rounding error since we round down in previewRedeem.

// Original Solidity excerpt: contracts/8/src/ATokenVault.sol:617-655
    function _baseDeposit(uint256 assets, uint256 shares, address depositor, address receiver, bool asAToken) private {
        // Need to transfer before minting or ERC777s could reenter.
        if (asAToken) {
            ATOKEN.transferFrom(depositor, address(this), assets);
        } else {
            UNDERLYING.safeTransferFrom(depositor, address(this), assets);
            AAVE_POOL.supply(address(UNDERLYING), assets, address(this), REFERRAL_CODE);
        }
        _s.lastVaultBalance = uint128(ATOKEN.balanceOf(address(this)));

        _mint(receiver, shares);

        emit Deposit(depositor, receiver, assets, shares);
    }

    function _baseWithdraw(
        uint256 assets,
        uint256 shares,
        address owner,
        address receiver,
        address allowanceTarget,
        bool asAToken
    ) private {
        if (allowanceTarget != owner) {
            _spendAllowance(owner, allowanceTarget, shares);
        }

        _burn(owner, shares);

        // Withdraw assets from Aave v3 and send to receiver
        if (asAToken) {
            ATOKEN.transfer(receiver, assets);
        } else {
            AAVE_POOL.withdraw(address(UNDERLYING), assets, receiver);
        }
        _s.lastVaultBalance = uint128(ATOKEN.balanceOf(address(this)));

        emit Withdraw(allowanceTarget, receiver, owner, assets, shares);
    }

// Original Solidity excerpt: contracts/8/src/ATokenVaultStorage.sol:14-20
    struct Storage {
        // total aToken incl. fees
        uint128 lastVaultBalance;
        // fees accrued since last updated
        uint128 accumulatedFees;
        // Deprecated storage gap
        uint40 __deprecated_gap;

