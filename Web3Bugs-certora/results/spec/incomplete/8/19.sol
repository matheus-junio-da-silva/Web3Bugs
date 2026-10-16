// Original Solidity excerpt: contracts/8/src/ATokenVault.sol:420-430
    function withdrawFees(address to, uint256 amount) public override onlyOwner {
        _accrueYield();
        require(amount <= _s.accumulatedFees, "INSUFFICIENT_FEES"); // will underflow below anyway, error msg for clarity

        _s.accumulatedFees -= uint128(amount);

        ATOKEN.transfer(to, amount);

        _s.lastVaultBalance = uint128(ATOKEN.balanceOf(address(this)));

        emit FeesWithdrawn(to, amount, _s.lastVaultBalance, _s.accumulatedFees);

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

// Original Solidity excerpt: contracts/8/src/ATokenVault.sol:508-522
    function _accrueYield() internal {
        uint256 newVaultBalance = ATOKEN.balanceOf(address(this));

        // Skip computation if there is no yield
        if (newVaultBalance <= _s.lastVaultBalance) {
            return;
        }

        uint256 newYield = newVaultBalance - _s.lastVaultBalance;
        uint256 newFeesEarned = newYield.mulDiv(_s.fee, SCALE, MathUpgradeable.Rounding.Down);

        _s.accumulatedFees += uint128(newFeesEarned);
        _s.lastVaultBalance = uint128(newVaultBalance);

        emit YieldAccrued(newYield, newFeesEarned, newVaultBalance);

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

